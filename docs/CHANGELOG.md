## [1.6.2](https://github.com/savannahghi/idr-server/compare/v1.6.1...v1.6.2) (2023-04-05)


### Bug Fixes

* GCS blobs signed URLS generation ([#61](https://github.com/savannahghi/idr-server/issues/61)) ([56209d9](https://github.com/savannahghi/idr-server/commit/56209d9f3fef94ec4404a50d72706e35fc405d31))


### Dependency Updates

* **deps:** update node dependencies ([#60](https://github.com/savannahghi/idr-server/issues/60)) ([3a7eca4](https://github.com/savannahghi/idr-server/commit/3a7eca4d26fb3cfd167615dfcf64c4fdc57a72bb))


### Refactors

* **conf:** migrate production static storage to GCS buckets ([#62](https://github.com/savannahghi/idr-server/issues/62)) ([fd816c8](https://github.com/savannahghi/idr-server/commit/fd816c894b24516973623388d967047278af3a50))
* **conf:** update storages configuration ([#63](https://github.com/savannahghi/idr-server/issues/63)) ([70b6244](https://github.com/savannahghi/idr-server/commit/70b624474254de58742f874b252105c8213811c6)), closes [/docs.djangoproject.com/en/4.2/releases/4.2/#psycopg-3](https://github.com/savannahghi//docs.djangoproject.com/en/4.2/releases/4.2//issues/psycopg-3)

## [1.6.1](https://github.com/savannahghi/idr-server/compare/v1.6.0...v1.6.1) (2023-04-04)


### Bug Fixes

* assorted fixes ([#55](https://github.com/savannahghi/idr-server/issues/55)) ([113aa02](https://github.com/savannahghi/idr-server/commit/113aa02e203ee3b57f2a7ebbde2b7a7552057bf8))
* **db:** database connection errors ([#56](https://github.com/savannahghi/idr-server/issues/56)) ([c9758d3](https://github.com/savannahghi/idr-server/commit/c9758d3787d04eb25491b4c77e7ccc58cc7b41a2))


### Dependency Updates

* **deps:** update project dependencies ([#54](https://github.com/savannahghi/idr-server/issues/54)) ([bd9cdb1](https://github.com/savannahghi/idr-server/commit/bd9cdb14978ed998384e0eeceed3b269b7f2d981))

## [1.6.0](https://github.com/savannahghi/idr-server/compare/v1.5.0...v1.6.0) (2022-10-17)


### Features

* integrate django channels into the project ([#49](https://github.com/savannahghi/idr-server/issues/49)) ([f20b763](https://github.com/savannahghi/idr-server/commit/f20b7637a55198242aa081174da0c237defca952))


### Dependency Updates

* **deps:** update python dependencies. ([#48](https://github.com/savannahghi/idr-server/issues/48)) ([d23207f](https://github.com/savannahghi/idr-server/commit/d23207fa49292ebc40b24aad722d8f7b2694e664))

## [1.5.0](https://github.com/savannahghi/idr-server/compare/v1.4.0...v1.5.0) (2022-09-27)


### Features

* add google analytics to track site usage. ([#45](https://github.com/savannahghi/idr-server/issues/45)) ([d290cf3](https://github.com/savannahghi/idr-server/commit/d290cf3bfb09f5c4dbf24ab721001e3c471afce0))


### Bug Fixes

* **ci:**  missing env variable error on deployment ([#46](https://github.com/savannahghi/idr-server/issues/46)) ([01e133b](https://github.com/savannahghi/idr-server/commit/01e133b049b504f7ce9e6f7c3a89a2bbcdf59996))

## [1.4.0](https://github.com/savannahghi/idr-server/compare/v1.3.0...v1.4.0) (2022-09-20)


### Features

* **admin:** add filters on the admin models ([#41](https://github.com/savannahghi/idr-server/issues/41)) ([5eb7e24](https://github.com/savannahghi/idr-server/commit/5eb7e249b6f3e1b644f37cf351d086038bb55e95))
* **api:** add missing API filters ([#42](https://github.com/savannahghi/idr-server/issues/42)) ([8aa1834](https://github.com/savannahghi/idr-server/commit/8aa1834bbf7e9e45bd27f03120d7d0e1d2a51bb4))
* integrate google analytics for user metrics collection ([#38](https://github.com/savannahghi/idr-server/issues/38)) ([974f1b4](https://github.com/savannahghi/idr-server/commit/974f1b45285f58d780e33c4c2eb26085975c772e))


### Dependency Updates

* **deps:** bump nth-check, cssnano and gulp-imagemin ([#29](https://github.com/savannahghi/idr-server/issues/29)) ([ade8b81](https://github.com/savannahghi/idr-server/commit/ade8b816807e798fd1ecf0ee9b22f65b7d20faf6))
* **deps:** update node version and node dependencies ([#44](https://github.com/savannahghi/idr-server/issues/44)) ([21d2865](https://github.com/savannahghi/idr-server/commit/21d28658a71f9117e8f3687c63f9b7f2b78ac51a))

## [1.3.0](https://github.com/savannahghi/idr-server/compare/v1.2.0...v1.3.0) (2022-09-11)


### Features

* Initial implementation for dashboards and visualizations app ([#15](https://github.com/savannahghi/idr-server/issues/15)) ([33a6306](https://github.com/savannahghi/idr-server/commit/33a6306788fddaf7fddab2fab43281270f5c766e))
* integrate pub/sub to notify new uploads ([#26](https://github.com/savannahghi/idr-server/issues/26)) ([d6ae0f1](https://github.com/savannahghi/idr-server/commit/d6ae0f1436d0720f59f50f04f830a349db3c7bfe))


### Bug Fixes

* **api:** add missing field on upload chunk creation ([#31](https://github.com/savannahghi/idr-server/issues/31)) ([4565996](https://github.com/savannahghi/idr-server/commit/4565996c5511bf00b0d431be5576b5097b694df0))
* **docker:** Dockerfile ([#24](https://github.com/savannahghi/idr-server/issues/24)) ([318ace2](https://github.com/savannahghi/idr-server/commit/318ace2e1bda07b856baa7788465b8e808c14572))
* drf missing static assets ([#25](https://github.com/savannahghi/idr-server/issues/25)) ([3b1e745](https://github.com/savannahghi/idr-server/commit/3b1e745d67f0e8cd245d8333826b856f954c50dd))
* **api:** erroneous upload chunk request data consumption ([#23](https://github.com/savannahghi/idr-server/issues/23)) ([759f3a8](https://github.com/savannahghi/idr-server/commit/759f3a8e37dfbd30f1bbf1fc093f285db1a76042))
* PubSub message creation ([#36](https://github.com/savannahghi/idr-server/issues/36)) ([0f9bf8a](https://github.com/savannahghi/idr-server/commit/0f9bf8a3956228747b0411c5916ee6c8b2133002))
* PubSub message to JSON conversion ([#37](https://github.com/savannahghi/idr-server/issues/37)) ([4962190](https://github.com/savannahghi/idr-server/commit/49621906cb087b056f10d96c435cc67d0b56987b)), closes [#36](https://github.com/savannahghi/idr-server/issues/36)


### Dependency Updates

* **deps:** bump django from 4.0.4 to 4.0.6 ([#16](https://github.com/savannahghi/idr-server/issues/16)) ([58e3455](https://github.com/savannahghi/idr-server/commit/58e34559983c2b5a51f58483459b5d18292498fa))
* **deps:** bump jquery-validation from 1.19.4 to 1.19.5 ([#17](https://github.com/savannahghi/idr-server/issues/17)) ([6f9aeee](https://github.com/savannahghi/idr-server/commit/6f9aeeebaa054d425515c934af6b8f13c232410f))
* **deps:** bump terser from 5.13.1 to 5.14.2 ([#19](https://github.com/savannahghi/idr-server/issues/19)) ([06e7956](https://github.com/savannahghi/idr-server/commit/06e79566f1a538fe50c3f78d480bc71ee33b30fa))


### Refactors

* **config:** add pub_sub_topic environment variable ([#34](https://github.com/savannahghi/idr-server/issues/34)) ([446cc4a](https://github.com/savannahghi/idr-server/commit/446cc4a1f6393b5aefe25fc93aefc26a2a1fe703))
* add unit tests ([#22](https://github.com/savannahghi/idr-server/issues/22)) ([ade99da](https://github.com/savannahghi/idr-server/commit/ade99da1745c310f454dc27d10bff134628c9fa6))
* data_source & metadata_extract filters ([#18](https://github.com/savannahghi/idr-server/issues/18)) ([07e6c6b](https://github.com/savannahghi/idr-server/commit/07e6c6b1dc5827ed00731fc3020f3c96cf2fad66))
* **conf:** improve project configuration ([#21](https://github.com/savannahghi/idr-server/issues/21)) ([f8e1614](https://github.com/savannahghi/idr-server/commit/f8e16143b63112e9de9362dda6fe156e295d7a6e))
* **pubsub:** refactor pubsub event trigger ([#30](https://github.com/savannahghi/idr-server/issues/30)) ([43f1c9a](https://github.com/savannahghi/idr-server/commit/43f1c9a9f5329aee687c14ed293ac6bda97840f1))
* **core:** refactor upload metadata architecture. ([#28](https://github.com/savannahghi/idr-server/issues/28)) ([781ec68](https://github.com/savannahghi/idr-server/commit/781ec68cca7be4b556102007ac49ff9b8f358c58))
* **api:** remove unneeded fields from the start upload chunk api. ([#27](https://github.com/savannahghi/idr-server/issues/27)) ([3a498b6](https://github.com/savannahghi/idr-server/commit/3a498b68a6076dc376281226c89938451f93b519))
