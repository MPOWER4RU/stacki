import stack.commands
import stack.gen

class Implementation(stack.commands.Implementation):
	def run(self, args):

		host = args[0]
		xml = args[1]

		c_gen = getattr(stack.gen,'Generator_%s' % self.owner.os)
		self.generator = c_gen()
		self.generator.setArch(self.owner.arch)
		self.generator.setOS(self.owner.os)

		if xml == None:
			xml = self.owner.command('list.host.xml', 
			[
			 host,
			 'os=%s' % self.owner.os,
			])
		self.runXML(xml, host)

	def runXML(self, xml, host):
		"""Reads the XML host profile and outputs Ubuntu
		preseed.cfg file"""
		
		# This method should addText something like
		#
		# <profile lang="preseed">
		# <section name="file-type-a"/>
		# <![CDATA[
		# ]]>
		# </section>
		# <section name="file-type-b"/>
		# <![CDATA[
		# ]]>
		# </section>
		# ...
		# </profile>
		#
		# This keeps everything in one command and the
		# output can easily be parsed and split into 
		# individual files.
		
		self.generator.parse(xml)
		self.owner.addOutput(host, '<profile lang="preseed.cfg">\n')
		self.get_section = ['main', 'packages', 'post', 'finish']
		
		for section in self.get_section:
			list = []
			list = self.generator.generate(section)
			#self.owner.addOutput(host, "<section name=\"%s\">" % section)
			#self.owner.addOutput(host, "<![CDATA[")
			self.owner.addOutput(host, "# %s"  % section)
			for line in list:
				self.owner.addOutput(host, line.rstrip())
			#self.owner.addOutput(host, "]]>")
			#self.owner.addOutput(host, "</section>")
		self.owner.addOutput(host, '</profile>\n')
