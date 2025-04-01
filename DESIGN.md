# Design Goals

This document covers the design goals for Skein.

- Maintainability is a core concern
- Prefer deep integration over new APIs
- Bevy Plugin and Addon boundaries

## Maintainability

Bevy updates every 3-4 months and building a large amount of infrastructure that highly abstracts and builds new concepts _could_ result in a better user experience _but_ the amount of time and people it takes to build and maintain unique concepts that increase the distance from core functionality is a cost that shouldn't be trivially accepted.

Example:

We could build a custom glTF asset processing pipeline to more directly integrate reflected components with scene spawning. This could become the base of powering new Relationship functionality. However, using a custom glTF asset processing pipeline means _not_ using the processing everyone else is using and distances the project further from integration with the rest of the ecosystem. The custom processing would have to maintain feature-compatibility with bevy's processing, etc.

### glTF over .blend

Blender's Python API is more stable than the .blend format and official word is that .blend file parsing isn't a viable target for integration.

## Prefer deep integration over new APIs

Whenever possible, Skein should prioritize supporting existing expected usage before creating new API abstractions.

Example:

Blender has at least 4 ways of duplicating and linking data (collection instances, duplicate objects (linked), duplicate objects (unlinked), Library Overrides). We should make sure each of them is supported before trying to build custom instancing or data-linking abstractions.

Similarly, using Bevy's `.spawn` APIs is preferred over building some special `.spawn_skein` API.

## Bevy Plugin and Addon boundaries

It would be painful for users if the Blender addon and the Bevy Plugin needed to be kept in lockstep versions. Users should be able to upgrade the Blender addon without worrying about it breaking their Bevy applications.

To this end, we should target API formats on both ends of integration. Going from Bevy to Blender we use BRP HTTP endpoints to communicate via a JSON format. Going from Blender to Bevy we target a `skein` field in the glTF Extras which is an array of directly consumable Component reflection data.

In the farther 0.16 release cycle future, maybe we can take advantage of BSN.
