- Images attached in zip, showing output and running cmds
- Make sure the 2 py files: s3.py and node.py are in same directory
================

CMD to run: python s3.py input_file.txt [optional arguments]

python s3.py rest.txt -tol 0.001 -iter 100

[user@snappy1 AI3]$ python s3.py cmu.txt -tol 0.001 -iter 100 -df 0.9


Use [-min True] when min is to be set while policy updation, otherwise ignore the '-min' argument : 
python s3.py rest.txt -tol 0.001 -iter 100 -min True

