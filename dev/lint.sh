#!/bin/bash
set -Eeuo pipefail

function func {
  ! grep -rn --color=always "$1" '{{cookiecutter.project_slug}}/'
}

func 'big_corporation_inc'
func 'Big Corporation Inc'
