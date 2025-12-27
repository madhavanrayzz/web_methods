FILE UPLOAD VULNERABILITY – LAB 1 (VERY SIMPLE NOTES)

1) Find upload feature
   - Image / file upload exists

2) Upload normal file
   - Upload: image.png
   - Confirms upload works

3) Intercept with Burp
   - Capture upload request
   - Change filename:
     image.png  →  image.php

4) PHP payload used
   <?php echo file_get_contents('/etc/passwd'); ?>

5) Upload modified request
   - Server accepts .php file

6) Access uploaded file
   - Open uploaded file URL in browser
   - Server executes PHP code
   - /etc/passwd content shown

RESULT
- Server-side code execution confirmed

WHY IT WORKED
- Server trusted file extension
- Upload directory was executable
- No proper server-side validation

BASIC BYPASS METHODS (CHECKLIST)

- Change extension:
  .php
  .phtml
  .php5
  .phar
  .php.jpg
  .jpg.php

- Fake Content-Type:
  Content-Type: image/png

- Bypass client-side checks:
  Use Burp / disable JS

- If execution blocked:
  Use file read payload:
  <?php echo file_get_contents('/etc/passwd'); ?>

REMEMBER (1 LINE)
- Web server decides EXECUTE vs STATIC based on extension



