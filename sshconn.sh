#!/bin/bash
ssh -L 7777:localhost:80 -L 5432:localhost:5432 ubuntu@54.211.134.148
