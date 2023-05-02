# FileNameSnapshot
A program for saving disk's file name, and print disk's file. 一个用于将磁盘全盘的文件名保存以及读取此保存文件的小程序。

# 简单说明
这是一个用于将磁盘遍历保存路径名及文件名的小程序，没什么大用，但是在你硬盘坏了的时候，你可以用这个程序生成的文件作为快照，检查出丢失了哪些重要的文件。

注意，本程序到现在为止只是个半成品！！！

仅仅是可以跑的程度。

# 简单使用
release里有两份exe，reader是读程序，writer是写程序，双击运行就行了，不过必须保证exe所在路径中有config.json配置文件。

writer生成的文件是db数据库文件。保存在与自身相同的路径下。

# config简单说明
congfig里可以设置的东西不多，主要是因为没什么可配置的，而且这个还是个半成品...

"db_name" 顾名思义，就是快照文件的文件名，默认为"SnapshotLs.db"，不建议修改。

"recursion_times" 这个直译是递归次数，其实就是保存的路径深度，默认为3，即保存的路径最大为3，例如: C:\Users\Dedicatus1979\Documents，这个路径的深度就是3，如果Documents文件夹下还有其他文件，则不会被记录在快照文件内。

"refuse"跟"accept"，这两个其实应该仔细说说。但我现在确实没时间，简单说吧，就是"refuse"里的路径将不会被快照保存，"accept"里的路径一定可以被保存。

可能会有人问，那"accept"有什么意义呢？这是因为这两个内容是可以用正则表达式表达的。accept的优先级高于refuse。

我们举例：
```
  "refuse": [
    "*/\\$.*",
    "*/\\..*",
    "/Bin",
    "*/.*\\.xml",
  ]
```
首先，我们用"/"表示windows系统中的文件路径标准"\\"，这是因为在json中"\\"是有特殊用途的，需要转义，所以我们干脆使用"/"作为路径的分隔符，就像liunx一样。

然后，如果第一个字符是"\*"则表示该路径是使用正则表达语法，例如我们例子中的第一行，这就表示我们拒绝的路径为"/\\$.*"含义是所有根目录下以"$"开头的路径。其中$用"\\$"表示是因为"$"在正则表达中有特殊含义，得转义。而实际我们写成"\\\\$"是因为json对"\\"有特殊含义，得用"\\\\"转义。

那第二行其实就是表达所有在根目录下以"."开头的路径被拒绝了。如果我们需要保留某个以"."开头的文件，我们可以在accept中添加，例如添加一个"/.xxx"这就表示"/.xxxx"这个路径被单独保留下来，前面可以加"\*"表示正则语法，也可不加，为什么就自己翻源码吧。

第三行没有"\*"所以它不是正则语法。表示的含义仅仅是"/Bin"路径被拒绝了。

第四行表示所有以".xml"的文件被拒绝了。

# 结尾
总之就这样吧，以后再慢慢改。

