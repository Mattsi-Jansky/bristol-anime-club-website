// Renders the raster images that live in public/ from their sources.
// Run with `npm run images` after changing the logo or the spring meetup photo,
// then commit the results.
//
//   public/og-image.jpg  1200×630 preview shown when the site is shared (Discord, WhatsApp…)
//   public/logo-512.png  the logo as a PNG, for search engines' structured data

import sharp from "sharp";
import { fileURLToPath } from "node:url";

const root = (path) => fileURLToPath(new URL(`../${path}`, import.meta.url));

const logo = root("public/logo.svg");
const photo = root("src/assets/photos/spring-meetup.jpg");

// Logo, rendered from the SVG at a fixed size.
const renderLogo = (size) => sharp(logo, { density: 300 }).resize(size, size).png();

await renderLogo(512).toFile(root("public/logo-512.png"));

// Share preview: the group photo cropped to 1200×630, keeping everyone's faces in
// frame, with the logo badge top-right over the sky and church tower (clear of faces).
const badge = await renderLogo(230).toBuffer();
const scaled = await sharp(photo).resize(1200).toBuffer(); // 1200×900
await sharp(scaled)
  .extract({ left: 0, top: 150, width: 1200, height: 630 })
  .composite([{ input: badge, top: 30, left: 1200 - 230 - 36 }])
  .jpeg({ quality: 82, mozjpeg: true })
  .toFile(root("public/og-image.jpg"));

console.log("Wrote public/logo-512.png and public/og-image.jpg");
