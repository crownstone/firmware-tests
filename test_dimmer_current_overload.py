import asyncio
from state_checker import *
from ble_base_test import BleBaseTest, BleBaseTestArgs
from base_test import BaseTestException

class TestDimmerCurrentOverload(BleBaseTest):
	@staticmethod
	def get_name() -> str:
		return __class__.__name__

	@staticmethod
	def get_description() -> str:
		return "Overload the dimmer (too much current), which should turn on the relay, and disable dimming."

	async def _run_ble(self):
		await self._run_with(100, 300, 400)
		await self._run_with(100, 2000, 3000)

	async def _run_with(self, dim_value: int, load_min: int, load_max: int):
		await self.setup()
		await self.set_switch(True, 0, False, False)
		self.user_action_request(f"Plug in a load of {load_min}W - {load_max}W.")

		# Check for the correct power usage.
		await PowerUsageChecker(self.state_checker_args, load_min, load_max).check()

		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()

		await self.set_switch(False, dim_value, True, True)
		await self.core.disconnect()

		# Expected error: current overload dimmer
		error_bitmask = 1 << 1
		await ErrorStateChecker(self.state_checker_args, error_bitmask).wait_for_state_match()

		# Relay should be turned on.
		await SwitchStateChecker(self.state_checker_args, 0, True).check()

		await self.connect()
		self.logger.info("Checking if dimming is disabled.")
		dimming_allowed = await self.core.state.getDimmingAllowed()
		if dimming_allowed:
			raise BaseTestException(f"Dimming allowed is {dimming_allowed}, should be {False}")

		await self.set_switch_should_fail(False, 100)

		await self.reset_errors()
