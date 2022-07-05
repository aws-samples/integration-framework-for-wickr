# Wickr Location Services

This example shows how to capture the Wickr device location messages which could be extended into other workflows.

## Configuration

#### Prerequisites

- Wickr Pro or Enterprise running
- You have an installed and configured Wickr IO Web Interface Bot (https://wickrinc.github.io/wickrio-docs/#existing-integrations-web-interface-integration)
- You have configured the Wickr callback server URL to be the AWS Gateway Endpoint from installing thids framework 

#### Wickr Location Room

When you install the Wickr Integration Framework you specified a location room called "TAK Locator"

1. Create a new Wickr room called "TAK Locator"
2. In any room where you have a running Wickr Web Interface bot as a user configured as per the prerequisites above share your device location:

<video width="320" height="240" controls>
  <source src="../assets/location-services.mp4" type="video/mp4">
</video>

## Results and Next Steps

After running the above you can now capture the coordinates from a Wickr device and integrate these with services such as [AWS Location Services](https://aws.amazon.com/location/)