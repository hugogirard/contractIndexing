targetScope = 'subscription'

@description('The location where the resources will be created')
param location string

@description('The resource group name')
param rgName string

resource rg 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: rgName
  location: location
}

var suffix = uniqueString(rg.id)

module doc 'br/public:avm/res/cognitive-services/account:0.13.2' = {
  scope: rg
  params: {
    tags: {
      SecurityControl: 'Ignore'
    }
    name: 'doc-${suffix}'
    kind: 'FormRecognizer'
    location: location
    sku: 'S0'
    disableLocalAuth: false
  }
}

module storage 'br/public:avm/res/storage/storage-account:0.27.1' = {
  scope: rg
  params: {
    tags: {
      SecurityControl: 'Ignore'
    }
    name: 'str${replace(suffix,'-','')}'
    kind: 'StorageV2'
    location: location
    publicNetworkAccess: 'Enabled'
  }
}

module aisearch 'br/public:avm/res/search/search-service:0.11.1' = {
  scope: rg
  params: {
    name: 'search-${suffix}'
    location: location
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
    partitionCount: 1
    replicaCount: 1
    sku: 'standard'
  }
}

output docIntelligenceResourceName string = doc.outputs.name
output docIntelligenceEndpoint string = doc.outputs.endpoint
output storageAccountName string = storage.outputs.name
output aiSearchResourceName string = aisearch.outputs.name
