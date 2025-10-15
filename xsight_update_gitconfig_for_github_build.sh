#!/bin/bash

update_urls() {

git config --global url."https://github.com/xsightlabs/sonic-sairedis.git".insteadOf \
	"http://x-git01.xsight.ent:7990/scm/xs/sonic-sairedis.git"

git config --global url."https://github.com/xsightlabs/sonic-swss".insteadOf \
	"http://x-git01.xsight.ent:7990/scm/xs/sonic-swss.git"

git config --global url."https://github.com/xsightlabs/sonic-utilities".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-utilities.git"

git config --global url."https://github.com/xsightlabs/sonic-platform-daemons.git".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-platform-daemons.git"

git config --global url."https://github.com/xsightlabs/sonic-platform-common.git".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-platform-common.git"

git config --global url."https://github.com/xsightlabs/x-SAI".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sai.git"

}

clear_urls() {

git config --global --unset url."https://github.com/xsightlabs/sonic-sairedis.git".insteadOf \
	"http://x-git01.xsight.ent:7990/scm/xs/sonic-sairedis.git"

git config --global --unset url."https://github.com/xsightlabs/sonic-swss".insteadOf \
	"http://x-git01.xsight.ent:7990/scm/xs/sonic-swss.git"

git config --global --unset url."https://github.com/xsightlabs/sonic-utilities".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-utilities.git"

git config --global --unset url."https://github.com/xsightlabs/sonic-platform-daemons.git".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-platform-daemons.git"

git config --global --unset url."https://github.com/xsightlabs/sonic-platform-common.git".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sonic-platform-common.git"

git config --global --unset url."https://github.com/xsightlabs/x-SAI".insteadOf \
	"https://bbk.xsightlabs.com/scm/xs/sai.git"

}

case "$1" in
  update)
    echo "Updating Xsight's Github URLs..."
    update_urls && echo "Done"
    ;;
  clear)
    echo "Clearing Xsight's Github URLs..."
    clear_urls && echo "Done"
    ;;
  *)
    echo "Invalid argument: $1"
    echo "Usage: $0 {update|clear}"
    exit 1
    ;;
esac

