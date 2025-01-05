async function generateFilename() {
  const title = await tp.user.input("Enter title:");
  const date = tp.date.now("YYYY-MM-DD");
  const slug = title.trim().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-");
  return `${date}-${slug}`;
}

export default generateFilename;