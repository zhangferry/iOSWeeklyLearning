#使用Homebrew来安装 Node 和 Watchman
brew install node
brew install watchman

# 使用nrm工具切换淘宝源
npx nrm use taobao

# 如果之后需要切换回官方源可使用
npx nrm use npm

# 安装 yarn
npm install -g yarn

echo "--->>> 👍 下载完毕"

# 创建项目
npx react-native init MoyuDemo
echo "--->>> 👍 创建项目"

cd MoyuDemo

yarn ios

