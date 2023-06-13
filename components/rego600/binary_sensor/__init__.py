import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
# from esphome.const import (
# )
from .. import ns, RegoInterfaceComponent, CONF_HUB_ID, CONF_REGO_VARIABLE

DEPENDENCIES = ['rego600']

REGO_PARAMETERS = {
    cv.Required(CONF_REGO_VARIABLE): cv.hex_uint16_t,
}

binary_sensor_schema = binary_sensor.binary_sensor_schema(
    ns.class_(
        "RegoBinarySensor",
        binary_sensor.BinarySensor,
        cg.PollingComponent,
    )
).extend(cv.polling_component_schema('10s')).extend(REGO_PARAMETERS)

CONF_DICT = {
    cv.Optional("connected"): binary_sensor_schema,
    cv.Optional("heat_needed"): binary_sensor_schema,
}

CONFIG_SCHEMA = cv.All(
    cv.has_at_least_one_key(*CONF_DICT.keys()),
    cv.Schema(
        {
            cv.GenerateID(CONF_HUB_ID): cv.use_id(RegoInterfaceComponent),
        }
    ).extend(CONF_DICT)
)


async def setup_conf(paren, config, key):
    if key in config:
        conf = config[key]
        var = await binary_sensor.new_binary_sensor(conf)
        await cg.register_component(var, conf)
        cg.add(var.register_hub(paren))
        cg.add(var.set_rego_variable(int(conf[CONF_REGO_VARIABLE])))
        # cg.add(paren.register_binary_sensor(str(key), var))


async def to_code(config):
    paren = await cg.get_variable(config[CONF_HUB_ID])
    for key in CONF_DICT.keys():
        await setup_conf(paren, config, key)
