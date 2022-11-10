import asyncio
from state_checker import *
from ble_base_test import BleBaseTest, BleBaseTestArgs
from base_test import BaseTestException


class TestDimmerCurrentHolds(BleBaseTest):
	def __init__(self, args: BleBaseTestArgs, load_min=120, load_max=160):
		super().__init__(args)
		self.load_min = load_min
		self.load_max = load_max

	@staticmethod
	def get_name() -> str:
		return __class__.__name__

	@staticmethod
	def get_description() -> str:
		return "Check if a high load on the dimmer, but within allowed specs, does not lead to an error."

	async def _run_ble(self):
		await self._run_with(100)
		await self._run_with(50)

	async def _run_with(self, dim_value: int):
		await self.setup()
		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()

		# Make it easy for the user to plug in the correct load.
		await self.set_switch(False, 100, True)

		self.user_action_request(f"Plug in a load of {self.load_min}W - {self.load_max}W.")

		await self.core.connect(self.address)
		await self.set_switch(False, dim_value, True)
		await self.core.disconnect()

		load_min = self.load_min
		load_max = self.load_max
		if (dim_value != 100):
			# Dimmed load won't scale perfectly
			load_min *= 0.75
			load_max *= 1.25

		await PowerUsageChecker(self.state_checker_args, int(load_min * dim_value / 100),
		                        int(load_max * dim_value / 100)).wait_for_state_match()
		await ErrorStateChecker(self.state_checker_args, 0).check()

		times = 10
		self.logger.info(f"Wait for {times} minutes")
		for i in range(0, times):
			await asyncio.sleep(1 * 60)
			await ErrorStateChecker(self.state_checker_args, 0).check()

		self.user_action_request("Place a phone next to the crownstone.")
		times = 10
		for i in range(0, times):
			self.user_action_request(f"Call the phone ({i} / {times}).")
			self.logger.info("Waiting 10 seconds ...")
			await asyncio.sleep(10)
			await ErrorStateChecker(self.state_checker_args, 0).check()

