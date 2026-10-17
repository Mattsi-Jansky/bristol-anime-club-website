# The Anime Club – Bristol & Beyond

The website for Bristol's anime club, at [bristolanimeclub.co.uk](https://bristolanimeclub.co.uk). It's a
static site built with [Astro](https://astro.build) and hosted on [Netlify](https://www.netlify.com).

## Making changes

Most edits don't need any code knowledge:

| To change…                                    | Edit                                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------ |
| The Discord invite, Facebook or Patreon links | `src/data/site.ts` (`links`)                                                         |
| The page title or Google description          | `src/data/site.ts` (`site`)                                                          |
| "What we get up to"                           | `src/data/site.ts` (`activities`)                                                    |
| "New to the club?" questions                  | `src/data/site.ts` (`faq`)                                                           |
| Slideshow photos                              | add the photo to `src/assets/photos/`, then list it in `src/data/site.ts` (`photos`) |
| Colours and fonts                             | `src/styles/tokens.css`                                                              |
| A section's wording or layout                 | its component in `src/components/`                                                   |

Small text changes can be made straight on GitHub: open the file, click the pencil icon and commit. Netlify
rebuilds and publishes the site a minute or two later.

### Photos

Commit photos as ordinary JPEGs, ideally around 2000px on the long side and with location data removed.
The build makes small AVIF and WebP copies at several sizes automatically, so there's no need to optimise
them by hand. The slideshow frame is 4:3: if a photo crops badly, set its `position` in `site.ts`
(for example `"50% 78%"` keeps the lower part in view).

Write a short `alt` description for every photo. It's what screen readers read out, and it helps Google.

## Working on it locally

You need Node.js 24 (see `.nvmrc`).

```sh
npm install
npm run dev        # live preview at http://localhost:4321
npm run check      # type checks and formatting check
npm run format     # fix formatting
npm run build      # build the finished site into dist/
npm run preview    # serve the built site
npm run images     # re-render the share image, logo PNG and icons in public/
```

## How it's put together

```
src/
  pages/index.astro         the page: puts the sections in order
  layouts/Base.astro        <head>: title, search and share tags, fonts, icons
  components/               one file per section, each with its own HTML and CSS
  data/site.ts              the club's words, links and photos
  styles/tokens.css         colours and fonts
  styles/global.css         base styles, buttons
  assets/photos/            slideshow photos (optimised at build time)
public/                     files served as-is: logo, favicons, share image, robots.txt
tools/make-images.mjs       renders the share image and icons (npm run images)
tools/logo/                 generates public/logo.svg (see its README)
```

Fonts are installed from npm with [Fontsource](https://fontsource.org) and served from the site itself, so
no visitor data goes to Google Fonts.

### Search engines

The page includes what Google uses to understand and show the site: a title and description that lead with
"Bristol Anime Club", structured data describing the club and its FAQ, a sitemap (`/sitemap-index.xml`),
`robots.txt`, and share previews for Discord, Facebook and WhatsApp. If the club's name, description or
profiles change, update `src/data/site.ts` and these all follow.

## Deploying

Netlify builds the site from the `main` branch using `netlify.toml`.

- Every push to `main` publishes the site.
- Every pull request gets its own preview link to check before merging.
- A deploy fails, and the live site stays as it was, if the build has errors or the page's Lighthouse
  scores drop below the thresholds in `netlify.toml`.
- GitHub Actions runs the same checks on every push and pull request (`.github/workflows/check.yml`), and
  Dependabot opens weekly pull requests to keep dependencies up to date.

### First-time setup

1. Push this repository to GitHub.
2. In Netlify, choose **Add new site → Import an existing project** and pick the repository. The build
   settings come from `netlify.toml`, so accept the defaults.
3. Under **Domain management**, add `bristolanimeclub.co.uk`. Set it as the primary domain, so
   `www.bristolanimeclub.co.uk` redirects to it, and point the domain's DNS at Netlify as instructed. Netlify
   adds HTTPS automatically.
4. In [Google Search Console](https://search.google.com/search-console), add the domain, verify it, and
   submit `https://bristolanimeclub.co.uk/sitemap-index.xml`.
