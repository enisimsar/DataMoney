# DataMoney

Simsar, E. and Caliskan, K. (2021) Twitter Interaction Data of Electra Cryptocurrency Community's Twitter Handle Followers and A Code for Follower Interaction Analysis. GitHub Repository https://github.com/enisimsar/DataMoney

[![DOI](https://zenodo.org/badge/345433383.svg)](https://zenodo.org/badge/latestdoi/345433383)

## Installation
- Database Part:
    - Install MongoDB from [here](https://docs.mongodb.com/manual/installation/).
    - Create MongoDB user and database
- Code Part:
    - This repository requires Python3.7
    - Install packages `pip install -r requirements.txt`

## Run the Collector Codes
- Before running the codes, you must fill `.env` file
    - `cp .env_example .env`
    - fill `.env` file according to your credentials

### Collector Part
- `1-get_profiles.py`: it collects the followers of `ElectraProtocol` profile.
- `2-get_followers.py`: it collects the follower information between collected profiles in the previous step.
- `3-get_mentions.py`: it collects the mention information between collected profiles in the first step. Please, be careful this code uses `api-v2` branch of the [tweepy](https://github.com/tweepy/tweepy.git) package.