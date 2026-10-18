// Everything about the club that the page shows, in one place.
// Edit the words and links here; the components only handle layout and style.

import type { ImageMetadata } from "astro";

import springMeetup from "../assets/photos/spring-meetup.jpg";
import christmasMeal from "../assets/photos/christmas-meal.jpg";
import modelKits from "../assets/photos/model-kits.jpg";
import retroGames from "../assets/photos/retro-games.jpg";
import boardGames from "../assets/photos/board-games.jpg";
import pubNight from "../assets/photos/pub-night.jpg";

export const site = {
  name: "The Anime Club - Bristol & Beyond",
  searchName: "Bristol Anime Club",
  url: "https://bristolanimeclub.co.uk",
  title: "Bristol Anime Club | The Anime Club – Bristol & Beyond",
  description:
    "A friendly anime club in Bristol for adults. Meetups every other Friday, watch parties, karaoke, screenings, and convention trips. Free to join, over-18s only.",
};

export const links = {
  discord: "https://discord.com/invite/FNwe9pBDha",
  socialGuide: "https://social.guide/groups/the-anime-club/",
};

export type Activity = { title: string; text: string };

export const activities: Activity[] = [
  {
    title: "Friday meetups",
    text: "Every other Friday we meet in person around Bristol. Pubs, board game cafés, and walks when the weather behaves.",
  },
  {
    title: "Watch parties and movie nights",
    text: "Online on Discord, so you can join in from the sofa.",
  },
  {
    title: "Karaoke",
    text: "Mostly anime openings. Nobody is judging your high notes.",
  },
  {
    title: "Screenings and premieres",
    text: "We go together to new anime films in Bristol cinemas, and sometimes book a private screening room.",
  },
  {
    title: "Conventions",
    text: "The “beyond” part: group trips to cons in Bristol and London.",
  },
];

export type Question = { question: string; answer: string };

// "New to the club?" answers. Keep these accurate: they're what newcomers (and Google) read.
export const faq: Question[] = [
  {
    question: "When and where do you meet?",
    answer:
      "Every other Friday, most often at Shredenhams near Cabot Circus but this can change. Check Discord! The venue and time for each meetup are posted there.",
  },
  {
    question: "How much does it cost?",
    answer: "Nothing, just come along and introduce yourself.",
  },
  {
    question: "Who can join?",
    answer:
      "Anyone aged 18 or over who enjoys anime or manga, whether you've watched hundreds of series or are just getting started.",
  },
  {
    question: "Do I need to know anyone?",
    answer:
      "No. It's a social club, so meeting new people is the point. It can help to say hello on Discord before your first meetup.",
  },
  {
    question: "Do I have to cosplay?",
    answer:
      "No, of course not! Most meetups have no cosplay, and when it is present it is welcome but entirely optional.",
  },
];

export type Photo = {
  src: ImageMetadata;
  alt: string;
  // Where to anchor the crop when the photo is fitted into the 4:3 frame.
  position?: string;
};

// The hero slideshow, in order. The first photo shows on load.
export const photos: Photo[] = [
  {
    src: springMeetup,
    alt: "Around thirty club members, several in anime cosplay, posing on the grass under a blossoming tree beside an old stone church wall.",
  },
  {
    src: christmasMeal,
    alt: "Club members in paper cracker crowns smiling around a restaurant table.",
  },
  {
    src: modelKits,
    alt: "Members building plastic model kits at a long wooden table covered in parts and instructions.",
  },
  {
    src: retroGames,
    alt: "A group of members posing in a retro games bar lined with consoles and arcade machines.",
  },
  {
    src: boardGames,
    alt: "Members laughing over a game at a pub table.",
    position: "50% 78%",
  },
  {
    src: pubNight,
    alt: "A big group squeezed into one selfie in a dark pub.",
  },
];
