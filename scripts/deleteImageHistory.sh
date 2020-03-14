cd ~/RedDoorLine
git checkout --orphan temp-branch
git add --all
git commit -am 'deleting history to prevent extended image record'
git branch -D master
git branch -m master
git push -f origin master
cd ~/
sudo rm -r ~/RedDoorLine
git clone https://github.com/d-nee/RedDoorLine.git