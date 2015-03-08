# pass-alfred
An alfred UI for the pass password manager (passwordstore.org)

This is a very simple wrapper. It is not smart enough to handle password-stores other than in the home directory, so that is a place that needs improvement. It autocompletes in Alfred for most of the commands that operate on existing passwords (I think the only exception is for cp), and passes through any input matching one of pass's commands unchanged to Terminal.app. 
