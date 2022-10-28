import os

import contextily
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.random import seed
from pysal.explore import esda
from pysal.lib import weights
from pysal.viz import splot
from splot.esda import lisa_cluster, plot_moran

DEFAULT_CRS = "EPSG:4326"


def load_brefix_data(brexit_data_dir: str) -> gpd.GeoDataFrame:
    os.path.join(brexit_data_dir, r"brexit_vote.csv")
    df_brexit_vote = pd.read_csv(
        os.path.join(brexit_data_dir, r"brexit_vote.csv"),
    )
    gdf_eu_districts = gpd.read_file(os.path.join(brexit_data_dir, r"local_authority_districts.geojson"))

    gdf_brexit = pd.merge(
        left=gdf_eu_districts, right=df_brexit_vote, how="inner", left_on="lad16cd", right_on="Area_Code"
    )
    return gdf_brexit


def create_choropleth_map(gdf: gpd.GeoDataFrame, target_col: str, draw_axes: Axes) -> Axes:
    gdf = gdf.to_crs(crs=DEFAULT_CRS)
    gdf.plot(
        column=target_col,
        cmap="viridis",
        scheme="quantiles",
        k=5,
        edgecolor="white",
        linewidth=0.0,
        alpha=0.75,
        legend=True,
        legend_kwds={"loc": 2},
        ax=draw_axes,
    )
    contextily.add_basemap(
        ax=draw_axes,
        crs=DEFAULT_CRS,
        source=contextily.providers.Stamen.TerrainBackground,
    )
    draw_axes.set_axis_off()

    return draw_axes


def compute_global_moran_i_statistic(
    gdf: gpd.GeoDataFrame, spatial_weight_matrix: weights.KNN, target_col: str
) -> esda.moran.Moran:
    moran_i_obj = esda.moran.Moran(y=gdf[target_col], w=spatial_weight_matrix)

    fig_obj, axes_obj = plot_moran(moran=moran_i_obj)
    fig_obj.savefig("Pct_Leave_moran_plot.jpg")

    return moran_i_obj


def compute_local_moran_i(gdf: gpd.GeoDataFrame, spatial_weight_matrix: weights.KNN, target_col: str):

    local_moran_i_obj = esda.moran.Moran_Local(y=gdf[target_col], w=spatial_weight_matrix)

    return local_moran_i_obj


class ChoroplethMapLISA:
    def create_local_moran_i_choropleth_maps(
        self, gdf: gpd.GeoDataFrame, local_moran_obj: esda.moran.Moran_Local
    ) -> Figure:
        gdf = gdf.to_crs(crs=DEFAULT_CRS)

        fig_obj, axes_obj = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))

        axes_obj = axes_obj.flatten()  # Make the axes accessible with single indexing

        axes_obj[0] = self._choropleth_local_statistic(axes_obj[0], gdf, local_moran_obj)
        axes_obj[1] = self._choropleth_quadrant_categories(axes_obj[1], gdf, local_moran_obj)
        axes_obj[2] = self._choropleth_significance_map(axes_obj[2], gdf, local_moran_obj)
        axes_obj[3] = self._choropleth_cluster_map(axes_obj[3], gdf, local_moran_obj)

        fig_obj.tight_layout()
        return fig_obj

    def _choropleth_local_statistic(
        self, axes_obj: Axes, gdf: gpd.GeoDataFrame, local_moran_obj: esda.moran.Moran_Local
    ) -> Axes:
        df_temp = gdf.assign(Is=local_moran_obj.Is)
        axes_obj = df_temp.plot(
            column="Is",
            cmap="plasma",
            scheme="quantiles",
            k=5,
            edgecolor="white",
            linewidth=0.1,
            alpha=0.75,
            legend=True,
            ax=axes_obj,
        )
        axes_obj = self._arrange_axis_obj(axes_obj, "local_moran_i_statistic")
        return axes_obj

    def _choropleth_quadrant_categories(
        self, axes_obj: Axes, gdf: gpd.GeoDataFrame, local_moran_obj: esda.moran.Moran_Local
    ) -> Axes:
        lisa_cluster(moran_loc=local_moran_obj, gdf=gdf, p=1, ax=axes_obj)  # 有意水準の設定(1に設定すると全てのObservationが有意として扱われる)
        axes_obj = self._arrange_axis_obj(axes_obj, "scatterplot_quadrant")
        return axes_obj

    def _choropleth_significance_map(
        self, axes_obj: Axes, gdf: gpd.GeoDataFrame, local_moran_obj: esda.moran.Moran_Local
    ) -> Axes:
        # Recode 1 to "Significant and 0 to "Non-significant"
        significance_dammy_val_series = pd.Series(
            data=1 * (local_moran_obj.p_sim < 0.05),  # Assign 1 if significant, 0 otherwise
            index=gdf.index,  # Use the index in the original data
        )
        df_temp = gdf.assign(significance_dammy=significance_dammy_val_series)
        axes_obj = df_temp.plot(
            column="significance_dammy",
            categorical=True,
            k=2,
            cmap="Paired",
            linewidth=0.1,
            edgecolor="white",
            legend=True,
            ax=axes_obj,
        )

        axes_obj = self._arrange_axis_obj(axes_obj, "statistical_significance")

        return axes_obj

    def _choropleth_cluster_map(
        self, axes_obj: Axes, gdf: gpd.GeoDataFrame, local_moran_obj: esda.moran.Moran_Local
    ) -> Axes:
        lisa_cluster(moran_loc=local_moran_obj, gdf=gdf, p=0.05, ax=axes_obj)

        axes_obj = self._arrange_axis_obj(axes_obj, "moran_cluster_map")

        return axes_obj

    def _arrange_axis_obj(self, axes_obj: Axes, axes_title: str) -> Axes:
        axes_obj.set_axis_off()
        axes_obj.set_title(label=axes_title)

        contextily.add_basemap(
            ax=axes_obj,
            crs=DEFAULT_CRS,
            source=contextily.providers.Stamen.TerrainBackground,
        )
        return axes_obj


def main():
    gdf_brexit = load_brefix_data(r"Statistics\Spatial Statistics\notebooks\data\brexit")
    print(gdf_brexit.head())

    fig_obj, axes_obj = plt.subplots(1, figsize=(9, 9))
    axes_obj = create_choropleth_map(gdf=gdf_brexit, target_col="Pct_Leave", draw_axes=axes_obj)
    fig_obj.savefig("Pct_Leave_choropleth_map.jpg")

    spatial_weight_matrix = weights.KNN.from_dataframe(df=gdf_brexit, k=8)
    spatial_weight_matrix.transform = "R"  # Row-standardization

    global_moran_obj = compute_global_moran_i_statistic(gdf_brexit, spatial_weight_matrix, "Pct_Leave")
    print(f"[LOG] moran i statistic: {global_moran_obj.I}")
    print(f"[LOG] empirical p-value: {global_moran_obj.p_sim}")

    local_moran_obj = compute_local_moran_i(gdf_brexit, spatial_weight_matrix, "Pct_Leave")
    print(f"[LOG] moran i statistic: {local_moran_obj.Is}")
    print(f"[LOG] empirical p-value: {local_moran_obj.p_sim}")

    choropleth_obj = ChoroplethMapLISA()
    fig_obj = choropleth_obj.create_local_moran_i_choropleth_maps(gdf_brexit, local_moran_obj)
    fig_obj.savefig("Pct_Leave_local_moran_i_choropleth_maps.jpg")


if __name__ == "__main__":
    main()
