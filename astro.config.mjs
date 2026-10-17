// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  // The live address. Used for canonical links, share previews and the sitemap.
  site: "https://bristolanimeclub.co.uk",
  // Pages are written as /page/index.html, so URLs end in a slash. Keep this
  // matching Netlify's "pretty URLs" so every page has exactly one address.
  trailingSlash: "always",
  // The site's CSS is small, so put it in the page rather than a separate,
  // render-blocking file.
  build: { inlineStylesheets: "always" },
  integrations: [sitemap()],
});
