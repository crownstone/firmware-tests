import asyncio
import logging
from state_checker import *
from ble_base_test import BleBaseTest, BleBaseTestArgs
from base_test import BaseTestException

class TestChipOverheat(BleBaseTest):
	# Same as config.
	CHIP_TEMP_THRESHOLD = 75

	CHIP_TEMP_MIN = CHIP_TEMP_THRESHOLD - 5
	CHIP_TEMP_MAX = CHIP_TEMP_THRESHOLD + 2
	CHIP_TEMP_COOL = CHIP_TEMP_THRESHOLD - 5


	@staticmethod
	def get_name() -> str:
		return __class__.__name__

	@staticmethod
	def get_description() -> str:
		return "Overheat the chip, which should turn off the relay."

	async def _run_ble(self):
		await self._run_with(True)
		await self._run_with(False)

	async def _run_with(self, setup_mode: bool):
		if setup_mode:
			await self.factory_reset()
		else:
			await self.setup()
		self.logger.info("Waiting for chip to cool off ...")
		await ChipTempChecker(self.state_checker_args, 0, self.CHIP_TEMP_COOL).wait_for_state_match(5 * 60)
		await DimmerReadyChecker(self.state_checker_args, True).wait_for_state_match()

		await self.set_switch(True, 0, True, True)
		await self.core.disconnect()

		self.user_action_request(f"Start heating up the chip, by blowing hot air on it. Make sure you don't heat up the dimmer.")

		# Expected error: chip temp overload
		error_bitmask = 1 << 2
		await ErrorStateChecker(self.state_checker_args, error_bitmask).wait_for_state_match(5 * 60)

		# Temperature should still be close to the threshold.
		await ChipTempChecker(self.state_checker_args, self.CHIP_TEMP_MIN, self.CHIP_TEMP_MAX).check()

		await ErrorStateChecker(self.state_checker_args, error_bitmask).check()

		# Relay should be turned off.
		await SwitchStateChecker(self.state_checker_args, 0, False).check()

		await self.set_switch_should_fail(True, 100)

		self.logger.info("Waiting for chip to cool off ...")
		await ChipTempChecker(self.state_checker_args, 0, self.CHIP_TEMP_COOL).wait_for_state_match(5 * 60)

		await self.reset_errors()
