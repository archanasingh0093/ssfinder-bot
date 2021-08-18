#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "cd63bf25-9704-4860-b122-4efeefed19ca")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "-CwW3tu6oq180~Ge~SX3Z8RcMuOS.X_Jw4")
