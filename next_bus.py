from botocore.vendored import requests
from datetime import datetime
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from bus.user_id_bus_table import get_user_bus_stop, put_user_bus_stop
from bus.bus import get_hour, get_minutes, get_next_bus

sb = StandardSkillBuilder(table_name="BusStopState", auto_create_table=True)


class LaunchRequestHandler(AbstractRequestHandler):
    # Handler for Skill Launch
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class NextBusIntentHandler(AbstractRequestHandler):
    # Handler for Next Bus Intent
    def can_handle(self, handler_input):
        return is_intent_name("NextBusIntent")(handler_input)

    def handle(self, handler_input):
        print(handler_input.request_envelope.request.intent.slots)
        if handler_input.request_envelope.request.intent.slots['number'].value:
            bus_stop = int(handler_input.request_envelope.request.intent.slots['number'].value)
        else:
            bus_stop = get_user_bus_stop(handler_input.request_envelope.session.user.user_id)
        
        print(handler_input.request_envelope.session.user.user_id)
        print("bus_stop: {}".format(bus_stop))
        
        if bus_stop:
            bus = get_next_bus(bus_stop)
            print(bus)
            d_time = bus['ExpectedDeparture']
            print(d_time)
            hour = get_hour(d_time)
            minutes = get_minutes(d_time)
            speech_text = "The next bus is due at {0} {1}".format(hour, minutes)
            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("When's the next bus?", speech_text)).set_should_end_session(
                True)
        else:
            attr = {}
            attr['bus_stop'] = 'unknown'
            handler_input.attributes_manager.persistent_attributes = attr
            handler_input.attributes_manager.save_persistent_attributes()
            speech_text = 'It looks like you have not yet set a default bus stop. Would you like to set one?'
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class YesIntentHandler(AbstractRequestHandler):
    # Handler for Yes Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        print("attr: {}".format(attr))
        if 'bus_stop' in attr:
            if attr['bus_stop'] == 'unknown':
                speech_text = "Please state the number of your default bus stop"
                handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

class BusStopIntentHandler(AbstractRequestHandler):
    # Handler for Bus Stop Intent
    def can_handle(self, handler_input):
        return is_intent_name("BusStopIntent")(handler_input)
        
    def handle(self, handler_input):
        stop_id = int(handler_input.request_envelope.request.intent.slots["number"].value)
        put_user_bus_stop(handler_input.request_envelope.session.user.user_id, stop_id)
        bus = get_next_bus(stop_id)
        print(bus)
        d_time = bus['ExpectedDeparture']
        print(d_time)
        hour = get_hour(d_time)
        minutes = get_minutes(d_time)
        speech_text = "The next bus is due at {0} {1}".format(hour, minutes)
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("When's the next bus?", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    # Handler for Help Intent
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "When's the next bus?", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    # Single handler for Cancel and Stop Intent
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("When's the next bus?", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    # Handler for Session End
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    # Catch all exception handler, log exception and
    # respond with custom message
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print("Encountered following exception: {}".format(exception))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NextBusIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(BusStopIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()