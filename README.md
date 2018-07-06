# Alexa, when's the next bus? (WIP) #

This is a very simple Alexa skill which allows the user to configure their closest bus stop (in Wellington, New Zealand), and to then ask Alexa when the next bus is that leaves from it.

## Using the skill ##

Invocate by saying:

```
Alexa, when is the next wellington bus
```

Configure a stop by telling Alexa your preferred stop number:
```
Alexa, my preferred stop is stop 7726
```

Ask Alexa when's the next bus:
```
Alexa, when's the next bus?
```

## Development ##

```bash
python3 -m venv .venv
. .venv/bin/activate.fish
pip install -r requirements.txt
pytest
```

To deploy to AWS Lambda, make sure you're authenticated in the command line and that you have terraform installed:

```
terraform init
terraform plan
terraform apply
```

The configuration inside the Alexa developer portal is currently manual. Follow [this](https://developer.amazon.com/alexa-skills-kit/tutorials/fact-skill-1) tutorial, which will give you enough to get going.

