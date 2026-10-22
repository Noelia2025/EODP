# LEVEL-1B MODULE

from l1b.src.initL1b import initL1b
from common.io.writeToa import writeToa, readToa
from common.src.auxFunc import getIndexBand
from common.io.readFactor import readFactor, EQ_MULT, EQ_ADD, NC_EXT
import numpy as np
import os
import matplotlib.pyplot as plt


class l1b(initL1b):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the L1B Processing Module")

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # ============================================================
            # Read TOA - output of the ISM in Digital Numbers
            # ============================================================

            toa = readToa(
                self.indir,
                self.globalConfig.ism_toa + band + '.nc'
            )


            # ============================================================
            # Equalization (radiometric correction)
            # ============================================================

            if self.l1bConfig.do_equalization:

                self.logger.info(
                    "EODP-ALG-L1B-1010: "
                    "Radiometric Correction (equalization)"
                )

                # Read multiplicative factor
                eq_mult = readFactor(
                    os.path.join(
                        self.auxdir,
                        self.l1bConfig.eq_mult + band + NC_EXT
                    ),
                    EQ_MULT
                )

                # Read additive factor
                eq_add = readFactor(
                    os.path.join(
                        self.auxdir,
                        self.l1bConfig.eq_add + band + NC_EXT
                    ),
                    EQ_ADD
                )

                # Apply equalization
                toa = self.equalization(
                    toa,
                    eq_add,
                    eq_mult
                )

                # Save equalized DN
                writeToa(
                    self.outdir,
                    self.globalConfig.l1b_toa_eq + band,
                    toa
                )


            # ============================================================
            # Restitution (absolute radiometric gain)
            # ============================================================

            self.logger.info(
                "EODP-ALG-L1B-1020: "
                "Absolute radiometric gain application (restoration)"
            )

            toa = self.restoration(
                toa,
                self.l1bConfig.gain[
                    getIndexBand(band)
                ]
            )


            # ============================================================
            # Write output TOA
            # ============================================================

            writeToa(
                self.outdir,
                self.globalConfig.l1b_toa + band,
                toa
            )

            self.plotL1bToa(
                toa,
                self.outdir,
                band
            )

            self.logger.info(
                "End of BAND " + band
            )

        self.logger.info(
            "End of the L1B Module!"
        )


    # ================================================================
    # EQUALIZATION
    # ================================================================

    def equalization(self, toa, eq_add, eq_mult):
        """
        Equalization. Apply an offset and a gain.

        :param toa: TOA in DN
        :param eq_add: Offset in DN
        :param eq_mult: Gain factor, adimensional
        :return: TOA in DN, equalized
        """

        toa = (toa - eq_add) / eq_mult

        return toa


    # ================================================================
    # RESTORATION
    # ================================================================

    def restoration(self, toa, gain):
        """
        Absolute Radiometric Gain - restore back to radiances.

        :param toa: TOA in DN
        :param gain: gain in [mW/m2/sr/DN]
        :return: TOA in radiances [mW/m2/sr]
        """

        toa = toa * gain

        self.logger.debug(
            'Sanity check. TOA in radiances after gain application '
            + str(toa[1, -1])
            + ' [mW/m2/sr]'
        )

        return toa


    # ================================================================
    # PLOT L1B TOA
    # ================================================================

    def plotL1bToa(self, toa_l1b, outputdir, band):

        plt.figure(figsize=(10, 6))

        plt.imshow(
            toa_l1b,
            aspect='auto'
        )

        plt.colorbar(
            label='Radiance [mW/m2/sr]'
        )

        plt.xlabel('ACT')
        plt.ylabel('ALT')

        plt.title(
            'L1B TOA Radiance - ' + band
        )

        savefile = os.path.join(
            outputdir,
            'l1b_toa_' + band + '.png'
        )

        plt.savefig(
            savefile,
            bbox_inches='tight'
        )

        plt.close()