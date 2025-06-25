# How to install and run bulk download tool

[Link to Adobe Wiki page for bulk download tool](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=ES&title=Updated+Bulk+Agreement+Download+Tool) 

1. Ensure that [Python 3 is installed](https://adobe.sharepoint.com/:w:/r/sites/AdobeSignLFS/_layouts/15/Doc.aspx?sourcedoc={C016BC20-2713-4D1C-8258-E37D70849982}&file=How to install Python 3.docx&action=default&mobileredirect=true) and that [installation has been troubleshooted if necessary](https://adobe.sharepoint.com/sites/AdobeSignLFS/_layouts/15/doc.aspx?sourcedoc={641fb46b-7ea7-4f88-a843-ed99223a2bd4}&action=edit). 
2. Create a new folder in a convenient location on your computer. 
3. Download the bulk download tool [source code](https://git.corp.adobe.com/Adobesign/download-tools/tree/main/agreements/src) (only three .py) files and put the .py files in the folder. 
4. Download the .py and .bat files from this SharePoint folder and put them in the same folder. 
5. Create an integration key with the scopes agreement_read:account, library_read:account, user_read:account, widget_read:account 
6. Edit bulk_download.bat (File > Open with) so as to substitute the integration key into \<integration key goes here\> 
7. Run bulk_download.bat file by double-clicking it. 

## download_webform_agreements

If you want to download all agreements originating from a web form, then follow the above steps, making the following modifications:

3. Download the get_webform_agreement_ids.py file from /download_webform_agreements and put it with the rest of your .py files.
4. Run download_webform_agreements.bat instead of bulk_download.bat.

### get_webform_agreement_ids.py

This program uses the Adobe Sign API to fetch all of the agreements associated with a web form of a given web form ID and then save the associated agreement senders and agreement IDs into a .csv file of a particular format. The format of the output .csv is 

```
sender,agr_id,secure_id 
<*owner of agreement with ID* <*id1*>>*,*<*id1*>,<*id1*> 
<*owner of agreement with ID* <*id2*>>*,*<*id2*>,<*id2*> 
<...> 
<*owner of agreement with ID* <*idN*>>*,*<*idN*>,<*idN*> 
```

So, an output CSV file might look like 

```
sender,agr_id,secure_id 
someemail1@org.com,aD3eF9cB-17Ca4bF2-Bd6aeE8c72A5f3dBaD3eF9c,aD3eF9cB-17Ca4bF2-Bd6aeE8c72A5f3dBaD3eF9c 
someemail2@org.gov,C4f7dEaB29fA3BcEdF0a2eB1-C5BaA8c4,C4f7dEaB29fA3BcEdF0a2eB1-C5BaA8c4
someemail3@org.net,bAeC12fA-E9dC4Ab137fEB2CdA6b4,bAeC12fA-E9dC4Ab137fEB2CdA6b4
```

