#!/usr/bin/env bash
heroku login
heroku create
git push heroku master
heroku ps:scale app=1
