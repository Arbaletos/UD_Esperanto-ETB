import npyscreen

class App(npyscreen.NPSAppManaged):
  def onStart(self):
      self.registerForm("MAIN", MainForm())

class MainForm(npyscreen.Form):
    def create(self):
        datumo = open('l40.con').read()
        datumo = datumo.split('\n')
        datumo = [d.split('\t') for d in datumo]
        for d in datumo:
            if len(d)<10:
                d = ['']*10

        #self.add(npyscreen.Textfield, name = "Text:", value="Forhundu!", relx=1, rely=1, max_width=20)
        #self.add(npyscreen.Textfield, name = "Text:", value="Forhundu!", relx=22, rely=1, max_width=20)
        self.add(npyscreen.SimpleGrid, name = 'Putin', columns=10, values=datumo)
    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__=='__main__':
    a = App()
    a.run()
