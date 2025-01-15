import os
import sys
import signal
import threading
import configparser
from threading import Lock

# packet ids
TelemetryPacketID_Engine = 6
TelemetryPacketID_CarStatus = 7
TelemetryPacketID_CarDamage = 10
TelemetryPacketID_LapTime = 2


class carTelemetry_Client:

    def __init__(self):
        print("Init carTelemetry client...")
        # init thread variables
        self.datastructure_lock = Lock()
        self.list_for_Ids = []
        self.id_To_LastPacket = {}
        # extract carTelemetry Data
        print("Connecting to extract CarTelemetry Data")

        self.carTelemetry = {}
        self.running = True

        self.Packets = [[6, 3], [6, 4], [7, 1]]

        self.thread = threading.Thread(target=self.loop, args=())
        self.thread.start()

    def getNextPacket(self):
        while self.running:
            try:
                # listen to the data via UDP channel
                packet = self.Packets.pop()
                packetID = packet[0]
                if packetID in [
                    TelemetryPacketID_Engine,
                    TelemetryPacketID_CarDamage,
                    TelemetryPacketID_CarStatus,
                    TelemetryPacketID_LapTime,
                ]:
                    with self.datastructure_lock:
                        if not packetID in self.list_for_Ids:
                            self.list_for_Ids.append(packetID)
                        self.id_To_LastPacket[packetID] = packet
            except Exception:
                continue

    def processTelemetryPacket_CarDamage(self, packet):
        print("processTelemetryPacket_CarDamage")
        processTelemetryPacket_Base(packet)

    def processTelemetryPacket_CarStatus(self, packet):
        print("processTelemetryPacket_CarStatus")
        processTelemetryPacket_Base(packet)

    def processTelemetryPacket_LapTime(self, packet):
        print("processTelemetryPacket_LapTime")
        processTelemetryPacket_Base(packet)

    def processTelemetryPacket_Engine(self, packet):
        print("processTelemetryPacket_Engine")
        processTelemetryPacket_Base(packet)

    def processTelemetryPacket_Base(self, packet):
        print("processTelemetryPacket_Base")

    def loop(self):
        print("Car Telemetry data loop started")

        thread_getNextPacket = threading.Thread(target=self.getNextPacket)
        thread_initPacketProcessing = threading.Thread(target=self.initPacketProcessing)
        thread_getNextPacket.start()
        thread_initPacketProcessing.start()
        thread_getNextPacket.join()
        thread_initPacketProcessing.join()

    def initPacketProcessing(self):
        while self.running:
            try:
                with self.datastructure_lock:
                    # Update packet ID
                    if len(self.list_for_Ids) > 0:
                        packetID = self.list_for_Ids.pop()
                        print("init, Get Packet with ID:", packetID)
                        packet = self.id_To_LastPacket[packetID]

            except Exception as e:
                print(repr(e))
                continue

    def shutdown(self):
        self.running = False
        self.consumer.shutdown()
        self.carTelemetry.close()
        self.thread.join()


print(__name__ == "__main__")

if __name__ == "__main__":
    print("HH")

if __name__ == "__main__":
    print("HI")
    print("<kuksa.val> Car Telemetry example feeder")
    client = carTelemetry_Client()
