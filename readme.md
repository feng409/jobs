# 自动投简历脚本

投得累了，不想挨个点，干脆筛选出目标职位列表，自动投递算了...

## install
```shell script
cp example.config.yaml config.yaml
vim config.yaml
# export browser cookie to json file
```

## boss 直聘

boss 的数据是渲染成静态页返回，因此直接 selenium 模拟点击，获取后疯狂打招呼

```python zhipin.py```

## 拉勾
待实现


## todo
- [ ] boss 模拟登录
- [ ] lagou 爬取思路及实现
- [ ] redis 记录投递过的，免再次打扰