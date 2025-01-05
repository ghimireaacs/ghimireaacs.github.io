<%*
function toSlug(title) {
    return title
        .toLowerCase()
        .normalize("NFD") // Normalize Unicode to remove accents/diacritics
        .replace(/[\u0300-\u036f]/g, "") // Remove diacritical marks
        .replace(/[^a-z0-9\s-]/g, "") // Remove invalid characters
        .trim() // Remove leading/trailing spaces
        .replace(/\s+/g, "-"); // Replace spaces with hyphens
}

async function generateFilename() {
  const title = await tp.system.prompt("Enter title:");
  if (!title) {
    throw new Error("Title is required to generate filename.");
  }
  const date = tp.date.now("YYYY-MM-DD");
  const slug = toSlug(title);
  return { filename: `${date}-${slug}`, title };
}

// No need to export the function, just call it directly in the Templater script
let title;
try {
  const { filename, title: generatedTitle } = await generateFilename();
  title = generatedTitle;
  await tp.file.rename(filename);
} catch (error) {
  console.error("Error generating filename:", error);
}
// Set up the front matter for a Jekyll post
-%>
---
layout: post
title: <%* tR += title %>
date: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ssZ") %>
draft: false
categories:
tags: 
description: "Some description"
image:
	path: /assets/img/headers/default.webp

---
