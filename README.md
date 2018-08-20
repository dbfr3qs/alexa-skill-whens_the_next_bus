# Alexa, when's the next bus? (WIP) #

This is a very simple Alexa skill which allows the user to configure their closest bus stop (in Wellington, New Zealand), and to then ask Alexa when the next bus is that leaves from it.

## Using the skill ##

Invocate by saying:

```
Alexa, tell me when is the next bus
```

If you have not yet set a stop, Alexa will ask you for your preferred stop number.

You can also ask for a specific stop at any time:

```
Alexa, tell me when is the next bus at stop {your-stop}
```

When invoked this way, Alexa will ask you if you want to set your preferred stop to this stop.

TODO:

You can also ask Alexa for a specific bus:

```
Alexa, tell me when is the next number {your-bus} bus
```

Or at a specific stop:

```
Alex, tell me when is the next number {your-bus} bus at stop {your-stop}
```

## Development ##

```bash
python3 -m venv .venv
. .venv/bin/activate.fish
pip install -r requirements-dev.txt
pytest
```

To deploy to AWS Lambda, make sure you're authenticated in the command line and that you have terraform installed:

```
cd infra
terraform init
terraform plan
terraform apply
```

The configuration inside the Alexa developer portal is currently manual. Follow [this](https://developer.amazon.com/alexa-skills-kit/tutorials/fact-skill-1) tutorial, which will give you enough to get going.

