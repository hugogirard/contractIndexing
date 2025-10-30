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
    name: 'doc-${suffix}'
    kind: 'FormRecognizer'
    location: location
    sku: 'S0'
  }
}
