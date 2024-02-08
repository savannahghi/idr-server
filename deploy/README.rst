IDR Server Deployment Chart
---------------------------
- This deployment chart is used for deploying `idr-server` to kubernetes_ cluster.
- The deployment involves two major steps:
    - deploying the app's container image to the project's google container registry (gcr)
    - deploying the image from gcr to kubernetes cluster.

Prerequisites
-------------

 **1. cluster:** Ensure you have created a kubernetes cluster to which the
  app will be deployed.
 **2. helm:** We use helm as our deployment tool. Make sure you have helm installed
  to the project's gcr. See `helm repo`_ on how to add helm to gcp project.
 **3. public domain:** In the context of `gcp` projects, you can achieve this by
  reserving a global static IP address and mapping the IP to a public domain.


TLS Cert management and External traffic control
------------------------------------------------

- This will be a `one-time setup` of the relevant objects in a cluster-wide context.
  We will use `cert-manager` for tls cert management and `kong` as our ingress controller.

- **First ensure to be in the right context by running:**

.. code-block:: console
  $ kubectl config get-contexts
  $ kubectl config use-context <cluster_name>

1. Install kong_ to serve as our ingress controller.

.. code-block:: console
   $ helm repo add kong https://charts.konghq.com
   $ helm repo update
   $ helm install kong/kong --generate-name \
   --set ingressController.installCRDs=false \
   --set proxy.loadBalancerIP=<your_static_IP> -n kong --create-namespace

2. Install cert-manager_ to handle tls certificates for the services.

.. code-block:: console
  $ helm repo add jetstack https://charts.jetstack.io
  $ helm repo update
  $ helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.11.0 \
  --set installCRDs=true

Next steps
-----------

- Once the above setup is complete, you are ready to execute routine deployments
  across various namespaces in the cluster. However, it is essential to configure
  specific environment variables.
- These variables will be sourced from both `Cloudbuild's trigger` and those stored
  in the `Secret Manager`


**CLOUDBUILD'S TRIGGER VARIABLES**

    +------------------------------------+--------------------------------+------------------------------------------+
    | VARIABLES                          | EXAMPLE VALUES                 | DESCRIPTION                              |
    +====================================+================================+==========================================+
    | _APP_NAME                          | idr server                     | The name of the application              |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _CLOUDSQL_INSTANCE_CONNECTION_NAME | prj_id:region:db_instance      | Cloud SQL DB connection string           |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _DEPLOYMENT_TYPE                   | test/play/prod                 | The target environment for deployment    |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _DOMAIN_NAME                       | test.cbs.fyj.org               | The domain name for accessing the app    |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _GKE_CLUSTER                       | fyj_cluster                    | The Kubernetes cluster for app deployment|
    +------------------------------------+--------------------------------+------------------------------------------+
    | _GKE_COMPUTE_ZONE                  | us-east-c                      | The kubernetes cluster zone              |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _GOOGLE_CLOUD_PROJECT              | fyj_prj_2030                   | GCP project id for the app               |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _IAM_SERVICE_ACCOUNT_KEY           | ghu453jb3e53jffhbfciujws783w   | Base64 encoded service account key       |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _IMAGE_NAME                        | docker.pkg.dev/idr-server-test | The App's docker image path              |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _DJANGO_SETTINGS_MODULE            | config.settings.gcp_k8ts       | The django configuration file            |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _PG_BOUNCER_HOST                   | pgbouncer-service              | The service name for pgbouncer           |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _PG_BOUNCER_PORT                   | 6432                           | PGBouncer service port                   |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _LETSENCRYPT_SERVER_TYPE           | letsencrypt-staging            | Letsencrypt's server environment         |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _NAMESPACE                         | test                           | The app's kubernetes cluster namespace   |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _PG_NAME                           | idr_test_db                    | The name of the application's database   |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _PG_USER                           | test_db_user                   | Database username                        |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _PG_PASSWORD                       | T3sTPassworlD                  | Database user password                   |
    +------------------------------------+--------------------------------+------------------------------------------+
    | _SETTINGS_NAME                     | idr_test_settings              | Secret manager secret name for the app   |
    +------------------------------------+--------------------------------+------------------------------------------+


**SECRET MANAGER SECRETS**

- The `configmap_job` plays a crucial role as the primary source of environment
  variables for the deployment process. Specifically, within the Django deployment
  templates, the configmap_job relies on the `secret manager` to generate the configmap
  file necessary for sourcing the required environment variables.
- As previously mentioned, the deployment occurs in two distinct phases. The initial
  phase encompasses the deployment of the application image and executing application
  migrations to update the database. In the subsequent phase, which involves deploying
  the same image to Kubernetes, it becomes imperative to override specific variable values.
- To ensure the seamless functioning of the service within the Kubernetes context,
  the configmap_job is designed to override the values of the following variables:

  +---------------------------+---------------------------+------------------------------------------+
  | VARIABLES                 | EXAMPLE VALUES            | DESCRIPTION                              |
  +===========================+===========================+==========================================+
  | DJANGO_SETTINGS_MODULE    | config.settings.gcp_k8ts  | App's Settings specific to k8ts context  |
  +---------------------------+---------------------------+------------------------------------------+
  | POSTGRES_HOST             | pgbouncer-service         | App's PG Host specific to k8ts context   |
  +---------------------------+---------------------------+------------------------------------------+
  | POSTGRES_PORT             | 6432                      | App's PG Port specific to k8ts context   |
  +---------------------------+---------------------------+------------------------------------------+

- To provide more context regarding the need for these changes, we utilize the `CloudSQL proxy`_ for connecting
  to our CloudSQL instance and leverage on PGBouncer_ as a service to effectively implement a connection pool mechanism.
  This strategy efficiently manages the volume of concurrent connections to the database and maintains a set of
  pre-established connections that can be reused.

Deployment
-----------
- Once the necessary variables have been set, run `git push` to any of the branches
  hooked to cloud triggers. This will trigger deployment to one of the namespaces
  specified in the `_NAMESPACE` variable.

**NOTE:**

- Helm executes files `lexicographically`; hence, the naming of the directories
  and manifest files in the templates folder follows the order of their dependencies
- Careful with names and passwords that contain special characters since `template rendering engine`_
  will most probably evaluate to changed variable values.
- Even with successful deployment, sometimes you may have delay in generation of `cert` and `key`
  for the ingress; **wait** for the cert to be generated.


.. _`kubernetes`: https://kubernetes.io/
.. _`helm repo`: https://github.com/GoogleCloudPlatform/cloud-builders-community/tree/master/helm
.. _`kong`: https://docs.konghq.com/kubernetes-ingress-controller/latest/install/helm/#helm
.. _`cert-manager`: https://cert-manager.io/docs/installation/helm/#installing-with-helm
.. _`template rendering engine`: https://helm.sh/docs/chart_template_guide/getting_started/
.. _`CloudSQL proxy`: https://cloud.google.com/sql/docs/postgres/connect-kubernetes-engine#run_the_in_a_sidecar_pattern
.. _`PGBouncer`: https://www.pgbouncer.org/
