FABRIC_MOD_JSON_EXAMPLE = """{
  "schemaVersion": 1,
  "id": "${mod_id}",
  "version": "${version}",
  "name": "${name}",
  "description": "${desc}",
  "authors": [
    "Me!"
  ],
  "contact": {
    "homepage": "https://fabricmc.net/",
    "sources": "https://github.com/FabricMC/fabric-example-mod"
  },
  "license": "CC0-1.0",
  "icon": "assets/icon.png",
  "environment": "*",
  "entrypoints": {
    "main": [
      "${package_name}.${main_class_name}"
    ],
    "client": [
      "${package_name}.${main_class_name}Client"
    ],
    "fabric-datagen": [
      "${package_name}.${main_class_name}DataGenerator"
    ]
  },
  "mixins": [
    "${mod_id}.mixins.json",
    {
      "config": "${mod_id}.client.mixins.json",
      "environment": "client"
    }
  ],
  "depends": {
    "fabricloader": ">=0.16.10",
    "minecraft": "~1.20.1",
    "java": ">=17",
    "fabric-api": "*"
  },
  "suggests": {
    "another-mod": "*"
  }
}"""
