IDR Server Deployment Chart
---------------------------
- This deployment chart is used for deploying `idr-server` to kubernetes_ cluster.
- The deployment involves two major steps:
    - deploying the app's container image to the project's google container registry (gcr)
    - deploying the image from gcr to kubernetes cluster.

Prerequisites
-------------

- **1. cluster:** Ensure you have created a kubernetes cluster to which the
  app will be deployed.
- **2. helm:** We use helm as our deployment tool. Make sure you have helm installed
  to the project's gcr. See `helm repo`_ on how to add helm to gcp project.
- **3. public domain:** In the context of `gcp` projects, you can achieve this by
  reserving a global static IP address and mapping the IP to a public domain.


TLS Cert management and External traffic control
------------------------------------------------

- This will be a `one-time setup` of the relevant objects in a cluster-wide context. We will
  use `cert-manager` for tls cert management and `kong` as our ingress controller.

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

    +------------------------------------------+-------+
    | VARIABLES                                | VALUE |
    +==========================================+=======+
    | _APP_NAME                                | <val> |
    +------------------------------------------+-------+
    | _CLOUDSQL_INSTANCE_CONNECTION_NAME       | <val> |
    +------------------------------------------+-------+
    | _DEPLOYMENT_TYPE                         | <val> |
    +------------------------------------------+-------+
    | _DOMAIN_NAME                             | <val> |
    +------------------------------------------+-------+
    | _GKE_CLUSTER                             | <val> |
    +------------------------------------------+-------+
    | _GKE_COMPUTE_ZONE                        | <val> |
    +------------------------------------------+-------+
    | _GOOGLE_CLOUD_PROJECT                    | <val> |
    +------------------------------------------+-------+
    | _IAM_SERVICE_ACCOUNT_KEY                 | <val> |
    +------------------------------------------+-------+
    | _IMAGE_NAME                              | <val> |
    +------------------------------------------+-------+
    | _K8TS_DJANGO_SETTINGS_MODULE             | <val> |
    +------------------------------------------+-------+
    | _K8TS_PG_HOST                            | <val> |
    +------------------------------------------+-------+
    | _K8TS_PG_PORT                            | <val> |
    +------------------------------------------+-------+
    | _LETSENCRYPT_SERVER_TYPE                 | <val> |
    +------------------------------------------+-------+
    | _NAMESPACE                               | <val> |
    +------------------------------------------+-------+
    | _PG_NAME                                 | <val> |
    +------------------------------------------+-------+
    | _PG_PASSWORD                             | <val> |
    +------------------------------------------+-------+
    | _PG_USER                                 | <val> |
    +------------------------------------------+-------+
    | _SETTINGS_NAME                           | <val> |
    +------------------------------------------+-------+

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

  +------------------------------------------+-------+
  | VARIABLES                                | VALUE |
  +==========================================+=======+
  | DJANGO_SETTINGS_MODULE                   | <val> |
  +------------------------------------------+-------+
  | POSTGRES_HOST                            | <val> |
  +------------------------------------------+-------+
  | POSTGRES_PORT                            | <val> |
  +------------------------------------------+-------+

- The `DJANGO_SETTINGS_MODULE` will be configured to point to a different
  configuration file. Similarly, `POSTGRES_HOST` should be updated to point to
  the pgbouncer service, and `POSTGRES_PORT` should be set to the pgbouncer port

**NOTICE:**

- Helm executes files lexicographically; hence, the naming of the directories
  and manifest files in the templates folder follows the order of their dependencies
- Careful with names and passwords that contain special characters since `template rendering engine`_
  will most probably evaluate to changed variable values.
- ...delay in generation of `cert` and `key` ...


.. _`kubernetes`: https://kubernetes.io/
.. _`helm repo`: https://github.com/GoogleCloudPlatform/cloud-builders-community/tree/master/helm
.. _`kong`: https://docs.konghq.com/kubernetes-ingress-controller/latest/install/helm/#helm
.. _`cert-manager`: https://cert-manager.io/docs/installation/helm/#installing-with-helm
.. _`template rendering engine`: https://helm.sh/docs/chart_template_guide/getting_started/
