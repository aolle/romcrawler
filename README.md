rom-crawler
===========

What is rom-crawler?
-----------------
A scrapy-based spider for automated search and web data extraction. It is be able to solve captcha codes through Optical character recognition (OCR) processes, create the required requests, control cookies and sessions to perform their job successfully. It allows you to choose memory or disk to save the data dump to work with this.


What do you need?
-----------------
The requirements are in the requirements.txt and system-requirements.txt files. The first one contains the requirements that you can install with pip, the last one can be in either way.

You must patch the pytesser.py requirement file with my provided custom patch named pytesser.py.patch.


Main properties, technologies and used libraries
------------------------------------------------
Programmed in Python under GNU/Linux.

Use of scrapy framework to build the crawler. <br>
Use of XML, JSON and XPath to work with data inputs.<br>
Use of parsers to get and parse some data.<br>
Use of custom patched pytesser to do ocr tasks.<br>
Use of context managing to make it easy some tasks.<br>
Use of operating system libraries to save data.<br>
Use of http methods to interact with destination.<br>
Use of PIP to install something.<br>
Use of diff and patch for patching.<br>
Use of virtualenv to make easy the python development.


License
-------
Licensed under GPLv3. Read LICENSE file.


--

Àngel Ollé Blázquez
