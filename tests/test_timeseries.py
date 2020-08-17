import datetime
import pdb

import pytest

from blackfynn import TimeSeries, TimeSeriesChannel
from blackfynn.models import TimeSeriesAnnotation, TimeSeriesAnnotationLayer


@pytest.fixture()
def timeseries(client, dataset):
    # create
    ts = TimeSeries("Human EEG")
    assert not ts.exists
    dataset.add(ts)
    assert ts.exists
    assert ts in dataset
    assert ts.type == "TimeSeries"
    assert ts.name.startswith(
        "Human EEG"
    )  # starts with bc duplicate names are appended
    ts2 = client.get(ts.id)
    assert ts2.id == ts.id
    assert ts2.name == ts.name
    assert ts2.type == "TimeSeries"
    del ts2

    # provide to other tests
    yield ts

    # remove
    dataset.remove(ts)
    assert not ts.exists
    assert ts not in dataset


@pytest.fixture()
def timeseries2(client, dataset):
    ts = TimeSeries("Animal EEG")
    dataset.add(ts)
    assert ts.exists
    yield ts
    dataset.remove(ts)


def test_update_timeseries_name(client, timeseries):
    # update timeseries: change name
    timeseries.name = "Monkey EEG"
    timeseries.update()
    timeseries2 = client.get(timeseries.id)
    assert timeseries2.id == timeseries.id
    assert timeseries2.name == timeseries.name
    assert timeseries2.type == "TimeSeries"


def test_timeseries_channels(client, timeseries):
    num_channels = 10

    assert timeseries.exists

    ts2 = client.get(timeseries.id)

    chs = []
    for i in range(num_channels):
        # init
        chname = "Channel-{}".format(i)
        ch = TimeSeriesChannel(name=chname, rate=256, unit="uV")
        assert not ch.exists

        # create
        timeseries.add_channels(ch)
        assert ch.exists
        assert ch.name == chname
        chs.append(ch)

        # use separate request to get channel
        ch.insert_property("key", "value")
        ch2 = [x for x in ts2.channels if x.id == ch.id][0]
        assert ch2.get_property("key") is not None
        assert ch2.name == ch.name
        assert ch2.type == ch.type
        assert ch2.rate == ch.rate
        assert ch2.unit == ch.unit
        del ch2

        # update channel
        ch.name = "{}-updated".format(ch.name)
        ch.rate = 200
        ch.update()

        # use separate request to confirm name change
        ch2 = [x for x in ts2.channels if x.id == ch.id][0]
        assert ch2.name == ch.name
        assert ch2.rate == ch.rate

    # ensure correct number of channels
    channels = timeseries.channels
    assert len(channels) == num_channels

    # get channels (via API)
    ch_ids = [x.id for x in channels]

    # check
    for ch in chs:
        assert ch.id in ch_ids

    ch = channels[0]
    timeseries.remove_channels(ch)
    channels = timeseries.channels
    assert len(channels) == num_channels - 1
    assert ch not in channels
    assert ch.id not in [x.id for x in channels]

    # remove by id
    ch_id = channels[0].id
    timeseries.remove_channels(ch_id)
    channels = timeseries.channels
    assert len(channels) == num_channels - 2
    assert ch_id not in [x.id for x in channels]


def test_timeseries_annotations(client, timeseries):
    assert timeseries.exists
    print("layers = ", timeseries.layers)

    # Create Layer
    layer1 = TimeSeriesAnnotationLayer(
        name="test_layer", time_series_id=timeseries.id, description="test_description"
    )
    a = layer1.as_dict()
    assert a["name"] == "test_layer"
    assert a["description"] == "test_description"

    # Add Layer
    timeseries.add_layer(layer1)
    assert layer1.exists

    # Get Layer
    layer1b = timeseries.get_layer("test_layer")
    assert layer1b.exists
    assert layer1b.name == "test_layer"
    assert layer1.id == layer1b.id
    assert layer1._api.timeseries is not None

    # Add another layer
    layer2 = timeseries.add_layer("test_layer2", "test_description2")
    assert layer2.exists

    layer2copy = timeseries.add_layer("test_layer2")
    assert layer2copy.id == layer2.id

    # Get Layer
    layer2b = timeseries.get_layer("test_layer2")
    assert layer2b.exists
    assert layer2b.name == "test_layer2"
    assert layer2.id == layer2b.id
    assert layer2._api.timeseries is not None

    layers = timeseries.layers
    assert len(layers) == 2
    assert set([layers[0].name, layers[1].name]) == set(["test_layer", "test_layer2"])

    # Create channels
    ch = TimeSeriesChannel(
        name="test_channel", rate=256, unit="uV", start=1, end=60 * 1e6
    )

    # Create annotation over one channel
    # create
    timeseries.add_channels(ch)
    assert ch.exists
    assert ch.id in [x.id for x in timeseries.channels]
    annot = TimeSeriesAnnotation(
        label="test_label",
        channel_ids=timeseries.channels[0].id,
        start=timeseries.channels[0].start,
        end=timeseries.channels[0].start + 1 * 1e6,
    )
    # Add Annotation
    layer1.add_annotations(annot)
    assert annot.exists

    # get annotations
    annotb = layer1.annotations()
    assert annotb[0].label == annot.label

    annotc = client._api.timeseries.get_annotation(timeseries, layer1, annot)
    assert annotc.label == annot.label

    # Create annotation over multiple channels
    ch2 = TimeSeriesChannel(
        name="test_channel", rate=256, unit="uV", start=1, end=60 * 1e6
    )

    timeseries.add_channels(ch2)
    channels = timeseries.channels
    ch_ids = [x.id for x in channels]
    assert ch2.exists
    assert ch2.id in ch_ids
    assert ch.id in ch_ids
    for ch in channels:
        assert ch.rate == 256
        assert ch.exists

    # add annotation over two channels
    channel_ids = [timeseries.channels[x].id for x in range(len(timeseries.channels))]

    annot2 = layer1.insert_annotation(
        annotation="test_label2",
        channel_ids=channel_ids,
        start=timeseries.channels[0].start + 1 * 1e6,
        end=timeseries.channels[0].start + 2 * 1e6,
    )

    assert annot2.exists

    annot_gen = layer1.iter_annotations(1)
    annot = next(annot_gen)
    assert annot[0].label == "test_label"
    next_annot = next(annot_gen)
    assert next_annot[0].label == "test_label2"

    ### TEST ANNOTATION COUNTS
    layer1_expected_counts = [
        {"start": 0, "end": 250000, "value": 1.0},
        {"start": 250000, "end": 500000, "value": 1.0},
        {"start": 500000, "end": 750000, "value": 1.0},
        {"start": 750000, "end": 1000000, "value": 1.0},
        {"start": 1000000, "end": 1250000, "value": 2.0},
        {"start": 1250000, "end": 1500000, "value": 1.0},
        {"start": 1500000, "end": 1750000, "value": 1.0},
        {"start": 1750000, "end": 2000000, "value": 1.0},
        {"start": 2000000, "end": 2000001, "value": 1.0},
    ]

    def _sort_counts(counts):
        return sorted(counts, key=lambda c: c["start"])

    assert (
        _sort_counts(
            timeseries.annotation_counts(
                start=timeseries.channels[0].start * 1e6,
                end=timeseries.channels[0].start + 2 * 1e6,
                layers=[layer1],
                period="0.25s",
            )[str(layer1.id)]
        )
        == layer1_expected_counts
    )
    assert (
        _sort_counts(
            layer1.annotation_counts(
                start=timeseries.channels[0].start * 1e6,
                end=timeseries.channels[0].start + 2 * 1e6,
                period="0.25s",
            )[str(layer1.id)]
        )
        == layer1_expected_counts
    )

    ### TEST DELETION

    annot3 = TimeSeriesAnnotation(
        label="test_label3",
        channel_ids=channel_ids,
        start=timeseries.channels[0].start + 1 * 1e6,
        end=timeseries.channels[0].start + 2 * 1e6,
    )
    layer1.add_annotations([annot2, annot3])
    annot3 = timeseries.add_annotations(layer=layer1, annotations=annot3)
    assert annot3.exists
    annot3.delete()
    assert not annot3.exists

    annot4 = timeseries.insert_annotation(
        layer=layer1,
        annotation="test_label3",
        start=timeseries.channels[0].start + 1 * 1e6,
        end=timeseries.channels[0].start + 2 * 1e6,
    )
    assert annot4.exists
    annot4.delete()
    assert not annot4.exists

    annot5 = timeseries.insert_annotation(
        layer="test_layer4",
        annotation="test_label3",
        start=timeseries.channels[0].start + 1 * 1e6,
        end=timeseries.channels[0].start + 2 * 1e6,
    )
    assert annot5.exists
    annot5.delete()
    assert not annot5.exists

    layer1.add_annotations([annot2, annot3])
    assert annot2.exists
    assert annot3.exists

    # test datetime input
    annot4 = timeseries.insert_annotation(
        layer="test_layer4",
        annotation="test_label3",
        start=datetime.datetime.utcfromtimestamp(
            (timeseries.channels[0].start + 1 * 1e6) / 1e6
        ),
        end=datetime.datetime.utcfromtimestamp(timeseries.channels[0].start + 2 * 1e6),
    )
    assert annot4.exists
    annot4.delete()
    assert not annot4.exists

    layer = timeseries.get_layer("test_layer4")
    assert layer.exists
    layer.delete()
    assert not layer.exists

    # delete annotations
    annot[0].delete()
    assert not annot[0].exists

    assert timeseries.exists
    timeseries.delete_layer(layer1)
    assert not layer1.exists

    assert layer2.exists
    layer2.delete()
    assert not layer2.exists


def test_timeseries_annotations_can_get_more_than_default_limit(timeseries):
    ch = TimeSeriesChannel(name="test_channel", rate=256, unit="uV", start=0, end=2e6)
    timeseries.add_channels(ch)

    layer = TimeSeriesAnnotationLayer(
        name="limit_layer",
        time_series_id=timeseries.id,
        description="layer with many small annotations",
    )
    timeseries.add_layer(layer)

    for i in range(200):
        annotation = TimeSeriesAnnotation(
            label="annotation_{}".format(i),
            channel_ids=ch.id,
            start=i * 1e4,
            end=(i + 1) * 1e4,
        )
        layer.add_annotations(annotation)

    # Should retrieve all annotations
    assert len(layer.annotations()) == 200

    # All of these annotations should be in the first 10-second window
    annots = next(layer.iter_annotations())
    assert len(annots) == 200

    layer.delete()


def test_timeseries_annotations_check_that_channels_belong_to_series(
    timeseries, timeseries2
):
    ch = TimeSeriesChannel(name="test_channel", rate=256, unit="uV", start=0, end=1e6)
    timeseries.add_channels(ch)
    print(timeseries, timeseries2)

    ch2 = TimeSeriesChannel(
        name="test_channel_2", rate=256, unit="uV", start=0, end=1e6
    )
    timeseries2.add_channels(ch2)

    layer = TimeSeriesAnnotationLayer(
        name="a_layer", time_series_id=timeseries.id, description="a layer"
    )
    timeseries.add_layer(layer)

    with pytest.raises(Exception):
        layer.annotations(channels=[ch, ch2])

    with pytest.raises(Exception):
        next(layer.iter_annotations(channels=[ch, ch2]))

    with pytest.raises(Exception):
        layer.annotation_counts(0, 1e6, period="0.1s", channels=[ch, ch2])


def test_timeseries_segments(client, timeseries):
    """
    No valid timeseries data to test against, but we can test the API calls.
    """
    channels = [
        TimeSeriesChannel(name="ch 1", rate=256, unit="uV"),
        TimeSeriesChannel(name="ch 2", rate=111.123, unit="uV"),
    ]
    timeseries.add_channels(*channels)

    for ch in timeseries.channels:
        ch.end = ch.start + 5e6
        ch.update()

        ch.segments()
        ch.segments(start=ch.start + 1e6)
        ch.segments(stop=ch.end - 1e6)
        ch.segments(stop=ch.end - 1e6, gap_factor=3)
        ch.segments(stop=ch.end - 1e6, gap_factor=33.33)
        ch.segments(stop=ch.end - 1e6, gap_factor=0.5)

    timeseries.segments()
    timeseries.segments(gap_factor=3)
    timeseries.segments(gap_factor=33.33)
    timeseries.segments(gap_factor=0.5)

    # TODO: API should soon error when value is non-numeric.
    #       Uncomment below when API is changed.

    with pytest.raises(Exception):
        timeseries.segments(gap_factor="should be int")

    with pytest.raises(Exception):
        ch.segments(gap_factor="should be int")
