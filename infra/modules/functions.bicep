param suffix string
param location string
param docIntelligenceResourceName string
param storageUploadDocumentResourceName string

var functionAppName = 'funcskill-${suffix}'
var deploymentStorageContainerName = 'app-package-${take(functionAppName, 32)}-${take(suffix, 7)}'

module userAssignedIdentity 'br/public:avm/res/managed-identity/user-assigned-identity:0.4.2' = {
  params: {
    name: 'func-${suffix}'
  }
}

module logAnalytics 'br/public:avm/res/operational-insights/workspace:0.11.1' = {
  params: {
    name: 'log-${suffix}'
    location: location
    dataRetention: 30
  }
}

module applicationInsights 'br/public:avm/res/insights/component:0.6.0' = {
  name: '${uniqueString(deployment().name, location)}-appinsights'
  params: {
    name: 'appli-${suffix}'
    location: location
    workspaceResourceId: logAnalytics.outputs.resourceId
    disableLocalAuth: true
  }
}

module storageFunction 'br/public:avm/res/storage/storage-account:0.25.0' = {
  name: 'storage'
  params: {
    name: 'strf${replace(suffix,'-','')}'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    dnsEndpointType: 'Standard'
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
    blobServices: {
      containers: [{ name: deploymentStorageContainerName }]
    }
    tableServices: {}
    queueServices: {}
    minimumTlsVersion: 'TLS1_2' // Enforcing TLS 1.2 for better security
    location: location
    tags: {
      SecurityControl: 'Ignore'
    }
  }
}

module appServicePlan 'br/public:avm/res/web/serverfarm:0.1.1' = {
  name: 'appserviceplan'
  params: {
    name: 'asp-${suffix}'
    sku: {
      name: 'FC1'
      tier: 'FlexConsumption'
    }
    reserved: true
    location: location
    zoneRedundant: false
  }
}

resource docIntelligence 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: docIntelligenceResourceName
}

module functionApp 'br/public:avm/res/web/site:0.16.0' = {
  name: 'functionapp'
  params: {
    kind: 'functionapp,linux'
    name: functionAppName
    location: location
    serverFarmResourceId: appServicePlan.outputs.resourceId
    managedIdentities: {
      userAssignedResourceIds: [
        userAssignedIdentity.outputs.resourceId
      ]
    }
    functionAppConfig: {
      deployment: {
        storage: {
          type: 'blobContainer'
          value: '${storageFunction.outputs.primaryBlobEndpoint}${deploymentStorageContainerName}'
          authentication: {
            type: 'UserAssignedIdentity'
            userAssignedIdentityResourceId: userAssignedIdentity.outputs.resourceId
          }
        }
      }
      scaleAndConcurrency: {
        maximumInstanceCount: 100
        instanceMemoryMB: 2048
      }
      runtime: {
        name: 'python'
        version: '3.11'
      }
    }
    siteConfig: {
      alwaysOn: false
    }
    configs: [
      {
        name: 'appsettings'
        properties: {
          // Only include required credential settings unconditionally
          AzureWebJobsStorage__clientId: userAssignedIdentity.outputs.clientId
          AzureWebJobsStorage__credential: 'managedidentity'
          AzureWebJobsStorage__blobServiceUri: 'https://${storageFunction.outputs.name}.blob.${environment().suffixes.storage}'
          AzureWebJobsStorage__queueServiceUri: 'https://${storageFunction.outputs.name}.queue.${environment().suffixes.storage}'
          AzureWebJobsStorage__tableServiceUri: 'https://${storageUploadDocumentResourceName}.table.${environment().suffixes.storage}'

          // Variables needed for the custom skills
          BLOB_ACCOUNT_URL: 'https://${storageUploadDocumentResourceName}.blob.${environment().suffixes.storage}'
          CONTAINER_NAME: 'documents'
          DOC_API_KEY: docIntelligence.listKeys().key1
          DOC_ENDPOINT: docIntelligence.properties.endpoint

          // Application Insights settings are always included
          APPLICATIONINSIGHTS_CONNECTION_STRING: applicationInsights.outputs.connectionString
          APPLICATIONINSIGHTS_AUTHENTICATION_STRING: 'ClientId=${userAssignedIdentity.outputs.clientId};Authorization=AAD'
        }
      }
    ]
  }
}

module rbacAssignments 'rbac.functions.bicep' = {
  name: 'rbacAssignments'
  params: {
    storageAccountFunctionName: storageFunction.outputs.name
    storageAccountDocumentName: storageUploadDocumentResourceName
    appInsightsName: applicationInsights.outputs.name
    userManagedIdentity: userAssignedIdentity.outputs.principalId ?? ''
  }
}

output functionAppResourceName string = functionApp.outputs.name
