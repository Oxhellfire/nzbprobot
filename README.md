# What is this repo about?

## Still Facing Issue to setup whole stuff?

### Join Support Group https://t.me/nzbpro

### NzbProBot is a Telegram bot written in python which interacts with NZBHydra and SABnzbd to provide direct download link

## NZBHydra

[NZBHydra](https://github.com/theotherp/nzbhydra) is a meta search engine for Usenet indexers. It allows users to search for content on multiple Usenet indexers simultaneously, providing a unified and convenient search experience. NZBHydra helps users find the content they are looking for across various Usenet sources, allowing them to quickly and efficiently access and download Usenet content.

Key Features:

- **Unified Search:** Search across multiple Usenet indexers in one place.
- **Search and Filter Options:** Provides advanced search and filter options for more precise results.
- **API Support:** Supports APIs for integration with other Usenet tools and applications.

## SABnzbd

[SABnzbd](https://sabnzbd.org/) is an open-source Usenet client that simplifies the process of downloading, verifying, and extracting Usenet files. It is designed to be easy to use and efficient, providing a user-friendly interface for managing Usenet downloads. SABnzbd supports automation through integration with various third-party tools, making it a popular choice for Usenet enthusiasts.

Key Features:

- **Automatic Downloading:** Automates the downloading, verification, and extraction of Usenet files.
- **Web Interface:** Provides a web-based user interface for easy management of downloads.
- **API Support:** Supports APIs.

## INDEXERS_WEBSITES

- **abNZB:** [https://abnzb.com/register](https://abnzb.com/register)
- **NZB Finder:** [https://nzbfinder.ws/register](https://nzbfinder.ws/register)
- **nzb.su:** [https://api.nzb.su/register](https://api.nzb.su/register)
- **NZBGeek:** [https://nzbgeek.info/register.php](https://nzbgeek.info/register.php)
- **NzBNooB:** [https://www.nzbnoob.com/register](https://www.nzbnoob.com/register)
- **nzbplanet:** [https://nzbplanet.net/registerpremium](https://nzbplanet.net/registerpremium)
- **altHUB:** [https://althub.co.za/register](https://althub.co.za/register)
- **Animetosho (Newznab):** [https://animetosho.org/register](https://animetosho.org/register)
- **miatrix:** [https://www.miatrix.com/register](https://www.miatrix.com/register)

## NzbProBot Usage

| COMMAND                                   | USAGE                                       |
| ----------------------------------------- | ------------------------------------------- |
| **/find** `<query>` or **/f** `<query>`   | For finding **`[Movies/Series/Books]`**     |
| **/movie** `<query>` or **/m** `<query>`  | For finding **`Movies`**                    |
| **/series** `<query>` or **/s** `<query>` | For finding **`Series`**                    |
| **/book** `<query>` or **/b** `<query>`   | For finding **`Books`**                     |
| **/indexers** or **/ind**                 | For checking all available **`Indexers`**   |
| **/add** `<ID>`                           | For downloading **`[Movies/Series/Books]`** |
| **/cancel**                               | It will cancel the **`Task`**               |
| **/cancelall**                            | It will cancel all **`Tasks`**              |

# Stuff Required for Bot

### You Need These Stuff For This Bot

- [newshosting](https://www.newshosting.com/) is an Usenet Provider
- [NZBHydra2](https://github.com/theotherp/nzbhydra2) is an Usenet Searcher
- [SABnzbd](https://github.com/sabnzbd/sabnzbd) is an Usenet Downloader
- [Rclone](https://rclone.org/drive/) for copying files to Google Drive
- And Any Indexers website **Need API Key of that Website**

# Setup for Bot

## 1. NEWSHOSTING

- **You just need username and password of this website**

## Before That install `tmux`

##### For Debian Based OS

```bash
hellfire@debian: sudo apt-get update
hellfire@debian: sudo apt-get install tmux
```

## 2. NZBHydra2

- Download Latest NZBHydra2 from [NZBHydra2](https://github.com/theotherp/nzbhydra2/releases/latest) release page and run that follow these commands

```bash
hellfire@debian: tmux new -t nzbhydra2
hellfire@debian: wget https://github.com/theotherp/nzbhydra2/releases/download/v5.3.5/nzbhydra2-5.3.5-amd64-linux.zip
hellfire@debian: unzip nzbhydra2-5.3.5-amd64-linux.zip
hellfire@debian: python3 nzbhydra2wrapperPy3.py

========= for deatching tmux session follow this ============
        ctrl+b then leave both buttons and press d
```

- It will run Locally on **`127.0.0.1:5076`** so we will forward the **`5076`** port for accessing on web to get API Key
- From your Machine use these commands to forward the port

```bash
hellfire@debian: ssh -L 5076:127.0.0.1:5076 <User>@<Your Vps IP>
```

- After that leave that ssh tab open and go to **`http://127.0.0.1:5076`** in your browser and go to **`Config`** then **`Main`** you will see **`API Key`** under Security section copy that and set in **`config.env`**

- For Adding Indexers go to **`Config`** then **`Indexers`** click on **`Add new indexer`** here under **`Usenet`** click on **`Choose from presets`** and choose your that index whose subscription/creds you have put **`API Key, Username and Password`** you can also add **`VIP Expiry`** not required tho it's just for reminder

```txt
##### N-Z-B-H-Y-D-R-A ####################################
H_IP=127.0.0.1
H_PORT=5076
H_API_KEY=<API Key Here>
```

Now you can close that tab where you ran **`ssh -L 5076:127.0.0.1:5076 <User>@<Your Vps IP>`** command **Note:- follow steps from here again to add more Indexers**

## 3. SABnzbd

- Download Latest SABnzbd from [SABnzbd](https://github.com/sabnzbd/sabnzbd/releases/latest) release page and run that follow these commands

```bash
hellfire@debian: tmux new -t sabnzbd
hellfire@debian: wget https://github.com/sabnzbd/sabnzbd/releases/download/4.2.1/SABnzbd-4.2.1-src.tar.gz
hellfire@debian: tar xf SABnzbd-4.2.1-src.tar.gz
hellfire@debian: cd SABnzbd-4.2.1
hellfire@debian: pip3 install -r requirements.txt
hellfire@debian: python3 SABnzbd.py -s 127.0.0.1:5000

========= for deatching tmux session follow this ============
        ctrl+b then leave both buttons and press d
```

- It will run Locally on **`127.0.0.1:5000`** so we will forward the **`5000`** port for accessing on web to setup SABnzbd
- From your Machine use these commands to forward the port

```bash
hellfire@debian: ssh -L 5000:127.0.0.1:5000 <User>@<Your Vps IP>
```

- After that leave that ssh tab open and go to **`http://127.0.0.1:5000`** in your browser **`SABnzbd Quick-Start Wizard`** in **Server Details**

```txt
host: news.newshosting.com
username: username of news.newshosting.com
password: password of news.newshosting.com
```

- Uncheck **`ssl`** Test Server if **`Connection Successful!`** then click on next go to **`Dashboard`** click on **`Config icon`**

#### Before proceeding further tick on "Advanced Settings"

- in **General** you will find **API Key** copy that and set in **`config.env`**

```txt
##### N-Z-B-H-Y-D-R-A ####################################
S_IP=127.0.0.1
S_PORT=5000
S_API_KEY=<Your API Key Here>
```

#### Folders

```txt
Temporary Download Folder: by-default it is "Downloads/incomplete" you can change if you want
Completed Download Folder: by-default it is "Downloads/complete" you can change if you want
Scripts Folder: nzbprobot/nzbpro/helpers

Save Changes
```

#### Categories

```txt
in 1st row choose script "postproc.py" click on save and don't change anythong here
```

#### Sorting

```txt
Click on "Add Sorter"
Name: Movie Sorting
Sort String: %title (%y)/%fn.%ext
Affected Job Types: Movies
Affected Categories: movies

CLick on "Add Sorter"

Name: Series Sorting
Sort String: %sn (%y)/Season %s/%fn.%ext
Affected Job Types: Series
Affected Categories: tv

CLick on "Add Sorter"
```

- Now you can close that tab where you ran **`ssh -L 5076:127.0.0.1:5076 <User>@<Your Vps IP>`**

## 4. Rclone

- Follow steps from here [Rclone](https://rclone.org/drive/)
- You will see something like this after finishing rclone setup

```txt
hellfire@debian: cat ~/.config/rclone/rclone.conf

[nzbpro]
type = drive
client_id = 382752603761-7e1oi16d47i7rm15hni1.apps.googleusercontent.com
client_secret = GOCSPX-yXSYi9Syghdx
scope = drive
token = {"access_token":"ya29.a0AfB_bOFAcPHK1HpSA2x0W8ifIIMPuD701XzI38lOPSBLUwSUJjT-li6oT3rJcluVvH-R9nDINkbPUiO7ARESFQHGX2MihFKfRu-bqfzdHOBBh7z-nA0173","token_type":"Bearer","refresh_token":"1//0gjl3iiiNDqN7CgYIARAAGBASNwF-L9Irm2oYEjiNz4g","expiry":"2024-01-07T22:25:17.363279344+05:30"}
team_drive =

========== Here "nzbpro" is remote name set that name in config.env ========
```

#### Done Now you can start nzbprobot

```bash
hellfire@debian: cd path/to/nzbprobot
hellfire@debian: pip3 install -r requirements.txt
hellfire@debian: python3 -m nzbpro
```
