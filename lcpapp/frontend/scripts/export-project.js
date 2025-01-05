const archiver = require('archiver');
const fs = require('fs');
const path = require('path');

// Create output directory if it doesn't exist
const outputDir = path.join(__dirname, '../exports');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir);
}

// Create a file to stream archive data to
const output = fs.createWriteStream(path.join(outputDir, `life-care-plan-${Date.now()}.zip`));
const archive = archiver('zip', {
  zlib: { level: 9 } // Sets the compression level
});

// Listen for all archive data to be written
output.on('close', function() {
  console.log(archive.pointer() + ' total bytes');
  console.log('Archive has been finalized and the output file descriptor has been closed.');
});

// Good practice to catch warnings (ie stat failures and other non-blocking errors)
archive.on('warning', function(err) {
  if (err.code === 'ENOENT') {
    console.warn(err);
  } else {
    throw err;
  }
});

// Good practice to catch this error explicitly
archive.on('error', function(err) {
  throw err;
});

// Pipe archive data to the file
archive.pipe(output);

// Add files and directories to include in the export
const directories = ['components', 'pages', 'public', 'styles'];
const files = ['package.json', 'next.config.js', 'tsconfig.json', 'tailwind.config.js', 'postcss.config.js'];

// Add directories
directories.forEach(dir => {
  const dirPath = path.join(__dirname, '..', dir);
  if (fs.existsSync(dirPath)) {
    archive.directory(dirPath, dir);
  }
});

// Add individual files
files.forEach(file => {
  const filePath = path.join(__dirname, '..', file);
  if (fs.existsSync(filePath)) {
    archive.file(filePath, { name: file });
  }
});

// Finalize the archive
archive.finalize();
