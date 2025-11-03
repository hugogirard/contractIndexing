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

module doc 'modules/docIntelligence.bicep' = {
  scope: rg
  params: {
    location: location
    suffix: suffix
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
    blobServices: {
      containers: [
        {
          name: 'documents'
        }
      ]
    }
  }
}

module function 'modules/functions.bicep' = {
  scope: rg
  params: {
    location: location
    suffix: suffix
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

// RBAC

@description('Built-in Role: [Storage Blob Data Reader]')
resource storageBlobDataReader 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
  scope: subscription()
}

@description('Built-in Role: [Storage Blob Data Contributor]')
resource storageBlobDataContributor 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  scope: subscription()
}

// Give Document Intelligence access reader of the Blob Storage
module doc_intelligence_storage_reader 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  scope: rg
  name: 'doc_intelligence_storage_reader'
  params: {
    #disable-next-line BCP321 use-safe-access
    principalId: doc.outputs.systemAssignedMIPrincipalId
    resourceId: storage.outputs.resourceId
    roleDefinitionId: storageBlobDataReader.id
  }
}

module doc_aiSearch_storage_contributor 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  scope: rg
  name: 'aisearch_storage_contributor'
  params: {
    #disable-next-line BCP321 use-safe-access
    principalId: aisearch.outputs.systemAssignedMIPrincipalId
    resourceId: storage.outputs.resourceId
    roleDefinitionId: storageBlobDataContributor.id
  }
}
