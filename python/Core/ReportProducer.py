__author__ = 'sbrochet'

import uuid

output_file_template = """    <File>
        <State Value="closed"/>
        <LFN></LFN>
        <PFN>%(pfn)s</PFN>
        <Catalog></Catalog>
        <ModuleLabel>output</ModuleLabel>
        <GUID>%(guid)s</GUID>
        <Branches></Branches>
        <OutputModuleClass>PoolOutputModule</OutputModuleClass>
        <TotalEvents>%(total_events)d</TotalEvents>
        <DataType>MC</DataType>
        <BranchHash>d41d8cd98f00b204e9800998ecf8427e</BranchHash>
        <Runs>
%(runs)s
        </Runs>
        <Inputs>
%(inputs)s
        </Inputs>
    </File>
"""

output_file_input_file_template = """            <Input>
                <LFN></LFN>
                <PFN>%(pfn)s</PFN>
                <FastCopying>0</FastCopying>
            </Input>
"""

input_file_template = """    <InputFile>
        <State Value="closed"/>
        <LFN></LFN>
        <PFN>%(pfn)s</PFN>
        <Catalog></Catalog>
        <ModuleLabel>source</ModuleLabel>
        <GUID>%(guid)s</GUID>
        <Branches>
        </Branches>
        <InputType>primaryFiles</InputType>
        <InputSourceClass>PoolSource</InputSourceClass>
        <EventsRead>%(events_read)d</EventsRead>
        <Runs>
%(runs)s
        </Runs>
    </InputFile>
"""

class Run:
    def __init__(self, run, lumi):
        self.run = run
        self.lumis = [lumi]

    def report_lumi_section(self, lumi):
        self.lumis.append(lumi)

    def merge(self, run):
        if self.run != run.run:
            raise TypeError('Trying to merge two runs with a different run number')

        self.lumis.extend(run.lumis)

    def __str__(self):
        """
        Return an XML representation of this class
        """
        xml = """            <Run ID="%d">\n""" % self.run
        self.lumis.sort()
        for lumi in self.lumis:
            xml += """                <LumiSection ID="%d" />\n""" % lumi
        xml += "            </Run>"

        return xml

class Runs:
    def __init__(self, runs=None):
        self.runs = runs if runs is not None else {}

    def report_lumi_section(self, run, lumi):
        if run in self.runs:
            self.runs[run].report_lumi_section(lumi)
        else:
            self.runs[run] = Run(run, lumi)

    def merge(self, runs):
        for run, data in runs.runs.items():
            if run in self.runs:
                self.runs[run].merge(data)
            else:
                self.runs[run] = data

    def __str__(self):
        """
        Return an XML representation of this class
        """
        xml = ""
        for run in sorted(self.runs.keys()):
            xml += str(self.runs[run])

        return xml

class ReportProducer:
    """
    Create a framework job report similar to the one created by CMSSW in order to trick CRAB.
    """

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.input_files = []
        self.output_file = {}
        pass

    def report_output_file(self, pfn):

        self.output_file = {'pfn': pfn, 'total_events': 0, 'guid': str(uuid.uuid4()).upper()}

    def report_input_file(self, pfn):
        """
        Report a new input file
        :param pfn: PFN of the new file
        :return: A token identifying this new file
        """
        f = {'pfn': pfn, 'events_read': 0, 'guid': str(uuid.uuid4()).upper(), 'runs': Runs()}
        self.input_files.append(f)

        token = len(self.input_files) - 1

        if 'input_files' in self.output_file:
            self.output_file['input_files'].append(token)
        else:
            self.output_file['input_files'] = [token]

        return token

    def report_event_read(self, input_token):
        if input_token >= len(self.input_files):
            raise ValueError('Invalid input file token')

        self.input_files[input_token]['events_read'] += 1

    def report_event_saved(self):
        self.output_file['total_events'] += 1

    def report_lumi_section(self, input_token, run, lumi):
        if input_token >= len(self.input_files):
            raise ValueError('Invalid input file token')

        self.input_files[input_token]['runs'].report_lumi_section(run, lumi)

    def save(self):
        with open(self.xml_file, 'w') as f:
            f.write(self.get_xml())

    def get_xml(self):
        xml = "<FrameworkJobReport>\n"

        xml += self._format_output_file()

        for token in range(0, len(self.input_files)):
            xml += self._format_input_file(token)

        xml += """    <ReadBranches>
    </ReadBranches>
    <PerformanceReport>
        <PerformanceSummary Metric="StorageStatistics">
            <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
            <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
            <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
            <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
            <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
            <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
        </PerformanceSummary>
    </PerformanceReport>
</FrameworkJobReport>"""

        return xml

    def _format_output_file(self):

        import copy

        runs = None
        input_files_xml = ""
        # Format input files
        for token in self.output_file['input_files']:
            input_file = self.input_files[token]
            input_files_xml += output_file_input_file_template % {'pfn': input_file['pfn']}

            if runs is None:
                runs = copy.deepcopy(input_file['runs'])
            else:
                runs.merge(input_file['runs'])

        self.output_file['inputs'] = input_files_xml
        self.output_file['runs'] = str(runs)

        return output_file_template % self.output_file

    def _format_input_file(self, input_token):
        return input_file_template % self.input_files[input_token]