# LEVEL-1C

from l1c.src.initL1c import initL1c
from common.io.writeToa import writeToa, readToa
from common.io.readGeodetic import readGeodetic, getCorners
import mgrs
import numpy as np
from scipy.interpolate import bisplrep, bisplev
import matplotlib.pyplot as plt
from common.io.l1cProduct import writeL1c
from matplotlib import cm


class l1c(initL1c):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the L1C Processing Module")

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # Read TOA - output of the L1B in Radiances
            # -------------------------------------------------------------------
            toa = readToa(
                self.l1bdir,
                self.globalConfig.l1b_toa + band + '.nc'
            )

            lat, lon = readGeodetic(
                self.gmdir,
                self.globalConfig.gm_geoloc
            )

            self.checkSize(lat, toa)

            # L1C reprojection onto the MGRS grid
            # -------------------------------------------------------------------
            lat_l1c, lon_l1c, toa_l1c = self.l1cProjtoa(
                lat,
                lon,
                toa,
                band
            )

            # Write output TOA
            # -------------------------------------------------------------------
            writeL1c(
                self.outdir,
                self.globalConfig.l1c_toa + band,
                lat_l1c,
                lon_l1c,
                toa_l1c
            )

            self.logger.info("End of BAND " + band)

        self.logger.info("End of the L1C Module!")

    def l1cProjtoa(self, lat, lon, toa, band):
        '''
        This function reprojects the L1B radiances into the MGRS grid.

        MGRS example:
        31REQ4367374067

        31 is the UTM zone
        R is the UTM latitude band
        EQ are the MGRS column and row band letters
        43673 is the MGRS Easting
        74067 is the MGRS Northing

        :param lat: L1B latitudes [deg]
        :param lon: L1B longitudes [deg]
        :param toa: L1B radiances
        :param band: band
        :return: L1C radiances, L1C latitude and longitude in degrees
        '''

        print("1 - Entrando en l1cProjtoa")

        # Create MGRS object
        # -------------------------------------------------------------------
        m = mgrs.MGRS()

        print("2 - MGRS creado")

        # Store unique MGRS positions
        # -------------------------------------------------------------------
        mgrs_tiles = set()

        for ii in range(toa.shape[0]):

            for jj in range(toa.shape[1]):

                auxi = m.toMGRS(
                    float(lat[ii, jj]),
                    float(lon[ii, jj]),
                    MGRSPrecision=int(
                        self.l1cConfig.mgrs_tile_precision
                    )
                )

                mgrs_tiles.add(auxi)

        print("3 - MGRS terminado")
        print("Numero de posiciones MGRS:", len(mgrs_tiles))

        mgrs_tiles = list(mgrs_tiles)

        # Initialise output arrays
        # -------------------------------------------------------------------
        toa_l1c = np.zeros(
            len(mgrs_tiles),
            dtype=np.float64
        )

        lat_l1c = np.zeros(
            len(mgrs_tiles),
            dtype=np.float64
        )

        lon_l1c = np.zeros(
            len(mgrs_tiles),
            dtype=np.float64
        )

        print("4 - Antes de preparar datos para bisplrep")

        # -------------------------------------------------------------------
        # Convert matrices to standard float64 vectors
        # -------------------------------------------------------------------
        lat_flat = np.asarray(
            lat,
            dtype=np.float64
        ).ravel()

        lon_flat = np.asarray(
            lon,
            dtype=np.float64
        ).ravel()

        toa_flat = np.asarray(
            toa,
            dtype=np.float64
        ).ravel()

        print("Numero original de puntos:", len(toa_flat))

        # -------------------------------------------------------------------
        # Remove possible NaN or infinite values
        # -------------------------------------------------------------------
        valid = (
            np.isfinite(lat_flat)
            & np.isfinite(lon_flat)
            & np.isfinite(toa_flat)
        )

        lat_flat = np.ascontiguousarray(
            lat_flat[valid],
            dtype=np.float64
        )

        lon_flat = np.ascontiguousarray(
            lon_flat[valid],
            dtype=np.float64
        )

        toa_flat = np.ascontiguousarray(
            toa_flat[valid],
            dtype=np.float64
        )

        print("Puntos validos:", len(toa_flat))

        print(
            "NaN lat:",
            np.isnan(lat_flat).sum()
        )

        print(
            "NaN lon:",
            np.isnan(lon_flat).sum()
        )

        print(
            "NaN toa:",
            np.isnan(toa_flat).sum()
        )

        print(
            "Rango lat:",
            np.min(lat_flat),
            np.max(lat_flat)
        )

        print(
            "Rango lon:",
            np.min(lon_flat),
            np.max(lon_flat)
        )

        print(
            "Rango toa:",
            np.min(toa_flat),
            np.max(toa_flat)
        )

        # -------------------------------------------------------------------
        # Check that enough valid data exist
        # -------------------------------------------------------------------
        if len(toa_flat) == 0:
            raise ValueError(
                "No valid data available for L1C interpolation"
            )

        print("5 - Antes de bisplrep")

        # -------------------------------------------------------------------
        # 2D spline interpolation
        # -------------------------------------------------------------------
        tck = bisplrep(
            lat_flat,
            lon_flat,
            toa_flat
        )

        print("6 - bisplrep terminado")

        # -------------------------------------------------------------------
        # Calculate L1C coordinates and radiances
        # -------------------------------------------------------------------
        for ii in range(len(mgrs_tiles)):

            lat_aux, lon_aux = m.toLatLon(
                mgrs_tiles[ii]
            )

            lat_l1c[ii] = float(lat_aux)
            lon_l1c[ii] = float(lon_aux)

            toa_l1c[ii] = bisplev(
                lat_l1c[ii],
                lon_l1c[ii],
                tck
            )

        print("7 - Interpolacion L1C terminada")

        return lat_l1c, lon_l1c, toa_l1c

    def checkSize(self, lat, toa):
        '''
        Check the sizes of the input radiances and geodetic coordinates.
        If they don't match, exit.

        :param lat: Latitude 2D matrix
        :param toa: Radiance 2D matrix
        :return: NA
        '''

        if lat.shape != toa.shape:

            raise ValueError(
                "Latitude and TOA dimensions do not match: "
                + str(lat.shape)
                + " != "
                + str(toa.shape)
            )