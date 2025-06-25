# Overview

This repository hosts migration and migration-adjacent scripts. Currently, there is:

* a [bulk_download.bat](#bulk_download_tool) batch script that orchestrates Python scripts so as to download PDFs of completed Adobe Sign agreements en masse
* a [download_webform_agreements.bat](#download_webform_agreements) script, which does the same thing as the first script but for agreements originating from Adobe Sign web forms
* a [get_template_ids.py](#get_template_idspy) Python script that can be used to save all Adobe Sign template IDs to a .csv file for use by other scripts

# bulk_download_tool

The bulk_download.bat bactch script orchestrates Python scripts so as to download PDFs of completed agreements en masse. To use it:

1. Ensure that [Python 3 is installed](https://adobe.sharepoint.com/:w:/s/AdobeSignLFS/ESC8FsATJxxNgljjfXCEmYIByHZqOM_XVohwH4z42f1K8g?e=Os7C7M) and that [installation has been troubleshooted if necessary](https://adobe.sharepoint.com/:w:/s/AdobeSignLFS/EWu0H2SnfohPqEPtmSI6K9QBw_UlWZ3i0chHbX977l6yoA?e=lNDdbK).
2. Create a new folder in a convenient location on your computer.
3. Download the bulk download tool [source code](https://git.corp.adobe.com/Adobesign/download-tools/tree/main/agreements/src) (constants.py, download.py, and restclient.py) and put the .py files in the folder from the previous step.
4. Download [bulk-download.bat](https://adobe.sharepoint.com/:u:/s/AdobeSignLFS/EQf3d2-WMtdOlZblCQaazkQBcE_iHNwVIEkBs6NnCx0hiA?e=7MK1Df).
5. Create an access token with the scopes `agreement_read:account`, `library_read:account`, `user_read:account`, and `widget_read:account`. See the [Manually creating access tokens](#Manually creating access tokens) section of this article for this.
6. Edit the .bat file and substitute the integration key into `<integration key goes here>`. 
7. Run the .bat file by double-clicking it.
   1. If double-clicking the .bat file doesn't work, then hold Shift, right click on the .bat file, and click "Copy as path". Then open a CMD window, paste (CTRL-V may not work- you may have to right click and then click "Paste"), and press Enter.

See the [Adobe Wiki](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=ES&title=Updated+Bulk+Agreement+Download+Tool) for more information about this tool.

## download_webform_agreements

If you want to download all agreements originating from a web form, then follow the same steps as before, but with the following modifications:

3. Download the get_webform_agreement_ids.py file from /download_webform_agreements and put it with the rest of your .py files.
4. Run download_webform_agreements.bat instead of bulk_download.bat.

### get_webform_agreement_ids.py

This program uses the Adobe Sign API to fetch all of the agreements associated with a web form of a given web form ID and then save the associated agreement senders and agreement IDs into a .csv file of a particular format. For my future reference, I am recording here that the format of the output .csv is 

```
sender,agr_id,secure_id 
<owner of agreement with ID> <id1>>,<id1>,<id1> 
<owner of agreement with ID <id2>>,<id2>,<id2> 
<...> 
<owner of agreement with ID <*dN>>,<idN>,<idN> 
```

So, an output CSV file might look like 

```
sender,agr_id,secure_id 
someemail1@org.com,aD3eF9cB-17Ca4bF2-Bd6aeE8c72A5f3dBaD3eF9c,aD3eF9cB-17Ca4bF2-Bd6aeE8c72A5f3dBaD3eF9c 
someemail2@org.gov,C4f7dEaB29fA3BcEdF0a2eB1-C5BaA8c4,C4f7dEaB29fA3BcEdF0a2eB1-C5BaA8c4
someemail3@org.net,bAeC12fA-E9dC4Ab137fEB2CdA6b4,bAeC12fA-E9dC4Ab137fEB2CdA6b4
```

### How to modify bulk download tools to work in government environment

If you want bulk_download_tool or download_webform_agreements to work in the government environment of Adobe Sign, you must perform all of the steps from the above and make the following changes:

3. Create an access token with the scopes `agreement_read:self`, `library_read:self`, `user_read:self`, and `widget_read:self` by using the government API swagger page. See the "Manually creating access tokens" section of this article for this.

3.5. After step 3, open constants.py in a text editor. CTRL-F for "INITIAL_HOST", and change the `INITIAL_HOST` value to the government API base URL, which is `"https://api.na1.adobesign.us:443"`. If you have already run the .bat file by following previous steps, then delete the folder named "dist" before you rerun the .bat file.

5. Follow the instructions in [Manually creating access tokens](#Manually creating access tokens) below to obtain an access token. Copy the portion of the access token that does *not* include "Bearer ". Then open the .bat file and paste this into `<integration key goes here>`.

# get_template_ids.py

get_template_ids.py is a Python command-line utility that saves all template IDs of templates accessible by the access token owner to a .csv file. This can be very useful when executing other programs that require such a .csv file as input.

Here is how to use the program:

1. Ensure that [Python 3 is installed](https://adobe.sharepoint.com/:w:/s/AdobeSignLFS/ESC8FsATJxxNgljjfXCEmYIByHZqOM_XVohwH4z42f1K8g?e=Os7C7M) on your computer and that [installation has been troubleshooted if necessary](https://adobe.sharepoint.com/:w:/s/AdobeSignLFS/EWu0H2SnfohPqEPtmSI6K9QBw_UlWZ3i0chHbX977l6yoA?e=lNDdbK).
2. Download get_template_ids.py from this repository.
3. Create an access token with the `library_read:account` scope if in commercial, and the `library_read:self` scope if in government.
4. Use the access token to run the Python program in a terminal session by executing `python get_template_ids.py --access_token <*access token*> --commercial` or `python get_template_ids.py --access_token <*access token*> --government`.

# Manually creating access tokens

## Commercial

Permanent access tokens may be created in commercial Sign. Here's how to manually create and gain access to one:

1. Have an Account Admin log into Adobe Sign and click on Admin.
2. Search "access tokens" in the left sidebar, and click on "Access Tokens".
3. On the new screen that comes up, click the plus inside the circle.
4. Select the desired scopes.
5. Scroll down and click Save.
6. Click on the row in the table corresponding to the access token you just created. Then click on the blue "Integration Key" text.
7. Copy the integration key.

## Government

Only temporary access tokens can be created in government Sign. Here's how to manually create and gain access to one:

1. Ensure that an API App has been created, where the owner of the API App is the email of the person who is going to be making API calls.
2. Have the owner of the API App go to the government [API Swagger page](https://secure.na1.adobesign.us/public/docs/restapi/v6#!). Click on /baseUris. *Click /baseUris again so that you can see a text field with grey text "Authorization" inside it.* Click Authorize on the right. A new pane should pop up.
3. Select the desired scopes.
4. Scroll down, and click yet another Authorize button. You may then be prompted with a login screen; if this happens, log in. Then approve all of the permissions by clicking "Allow Access".
5. You will be redirected back to the API Swagger page, except now text such as "Bearer aE606FcAcc194C3a9qFkl", which is an access token, has been inserted into the Authorization field.
