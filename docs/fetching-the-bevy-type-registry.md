---
title: Fetching the Bevy Type Registry
description: To work with Skein in Blender, the Components from your Bevy App must be fetched and processed
opengraph_image: /opengraph/opengraph-fetching-the-bevy-type-registry.jpg
---

## Prerequisites

To work with any Bevy Components in Blender, you have to run the `FetchRemoteTypeRegistry` operator, which is labelled as "Fetch a Remote Type Registry" in the Blender UI. This requires:

1. Having the **SkeinPlugin** installed in your Bevy App
   - Alternatively, you can set up the [`RemotePlugin`](https://docs.rs/bevy/latest/bevy/remote/struct.RemotePlugin.html) yourself
2. **Running** the Bevy App so it can serve the Bevy Remote Protocol endpoint
3. Having the **Skein Blender Addon** installed.

## The Registry Fetch Operator

Once you have a Bevy App with the Skein Plugin running, and the Blender Addon installed, you can fetch the Bevy type registry information one of three ways:

- Going to the `Edit` menu and choosing the **"Fetch a Remote Type Registry"** option
  ![edit menu](/images/introduction/edit-menu.avif)
- Clicking the button in any Skein Panel (Object, Mesh, or Material sections)
  ![skein panel](/images/introduction/skein-panel.avif)
- Using Blender's Search functionality to search directly for the Operator
  ![search](/images/introduction/search-menu.avif)

## What does this do?

Fetching the type registry information will query your Bevy App for the Component data you, Bevy, and third-party crates have registered. This data is then used as the basis for the Component selection list and form data for inserting Components onto objects in Blender.

If you change the Components by modifying existing Components or adding new ones, you will have to re-run the Fetch operator to fetch and process the new data.

Once the data is fetched, it is cached inside of the `.blend` file, so you don't need to have the Bevy application running while working in Blender unless you want to update the registry information to access new Component types.
