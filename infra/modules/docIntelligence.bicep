param suffix string
param location string

resource doc 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: 'doc-${suffix}'
  location: location
  kind: 'FormRecognizer'
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'doc-${suffix}'
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    allowProjectManagement: false
    publicNetworkAccess: 'Enabled'
  }
}

output systemAssignedMIPrincipalId string = doc.identity.principalId
