/* port number */
export const port = 5000;
export function fortune() {
  const i = Math.floor(Math.random() * 2);
  return ["小吉", "大吉"][i];
}
