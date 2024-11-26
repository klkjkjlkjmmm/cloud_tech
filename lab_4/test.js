const fs = require('fs');

test('index.html exists', () => {
  const fileExists = fs.existsSync('./index.html');
  expect(fileExists).toBe(true);
});

test('image exists', () => {
  const imageExists = fs.existsSync('./hamster.jpg');
  expect(imageExists).toBe(true);
});
