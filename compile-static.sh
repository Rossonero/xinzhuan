#!/bin/bash

cd xinzhuan/static/css
lessc style.less -x > style.css && cat bootstrap.min.css style.css timeline.css > all.css
