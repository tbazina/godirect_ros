# Single grip force signal reading in N. This message is appropriate for measuring
# pinching or gripping force produced from hand dynamometer.
Header header           # timestamp of the measurement
                        # frame_id is measurement type: pinch/grip
float32 grip_force     # Absolute grip force reading in N