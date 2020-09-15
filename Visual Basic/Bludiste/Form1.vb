
Public Class Form1
    Private sTime As DateTime
    Dim cheat As Boolean
    Dim result As Integer
    Private Sub zacatek()
        Dim startingPoint = Panel1.Location

        startingPoint.Offset(10, 10)

        Cursor.Position = PointToScreen(startingPoint)
        Timer1.Interval = 1000
        Timer1.Start()
        Label38.Show()
        Label39.Show()
        Label40.Show()
        Label41.Show()
        Label42.Show()
        Label43.Show()
        Label44.Show()
        Label45.Show()
        Label46.Show()
        Label47.Show()
        Label47.Show()
        Label48.Show()
        Label49.Show()
        Label50.Show()
        Label51.Show()
        Label52.Show()
        Label53.Show()
    End Sub
    Private Sub konec_MouseEnter(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles konec.MouseEnter
        Timer1.Stop()
        result = 10000 / Format(sTime, "ss")
        Label35.Text = result
        Label38.Hide()
        Label39.Hide()
        Label40.Hide()
        Label41.Hide()
        Label42.Hide()
        Label43.Hide()
        Label44.Hide()
        Label45.Hide()
        Label46.Hide()
        Label47.Hide()
        Label48.Hide()
        Label49.Hide()
        Label50.Hide()
        Label51.Hide()
        Label52.Hide()
        Label53.Hide()
        If MsgBox("Chcete hrát znovu?", vbYesNo) = vbNo Then
            MessageBox.Show("Bravo!!! " + Format(sTime, "mm:ss"))
            Close()
        Else
            zacatek()
            sTime = "00:00:00"
            Timer1.Start()
        End If
    End Sub
    Private Sub dotknutizdi(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label31.MouseEnter, Label9.MouseEnter, Label8.MouseEnter, Label7.MouseEnter, Label6.MouseEnter, Label5.MouseEnter, Label4.MouseEnter, Label34.MouseEnter, Label33.MouseEnter, Label32.MouseEnter, Label30.MouseEnter, Label3.MouseEnter, Label29.MouseEnter, Label28.MouseEnter, Label27.MouseEnter, Label26.MouseEnter, Label25.MouseEnter, Label24.MouseEnter, Label23.MouseEnter, Label22.MouseEnter, Label21.MouseEnter, Label20.MouseEnter, Label2.MouseEnter, Label19.MouseEnter, Label18.MouseEnter, Label17.MouseEnter, Label16.MouseEnter, Label15.MouseEnter, Label14.MouseEnter, Label13.MouseEnter, Label12.MouseEnter, Label11.MouseEnter, Label10.MouseEnter, Label1.MouseEnter
        zacatek()
    End Sub
    Public Sub New()

        InitializeComponent()

        zacatek()

    End Sub
    Private Sub teleport(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label36.MouseEnter, Label37.MouseEnter
        Label38.Hide()
        Label39.Hide()
        Label40.Hide()
        Label41.Hide()
        Label42.Hide()
        Label43.Hide()
        Label44.Hide()
        Label45.Hide()
        Label46.Hide()
        Label47.Hide()
        Dim startingPoint = Panel1.Location

        startingPoint.Offset(400, 440)

        Cursor.Position = PointToScreen(startingPoint)
    End Sub
    Private Sub mapa39(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label39.MouseEnter
        Label38.Hide()
    End Sub
    Private Sub mapa40(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label40.MouseEnter
        Label39.Hide()
    End Sub
    Private Sub mapa41(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label41.MouseEnter
        Label40.Hide()
    End Sub
    Private Sub mapa42(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label42.MouseEnter
        Label41.Hide()
    End Sub
    Private Sub mapa43(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label43.MouseEnter
        Label42.Hide()
    End Sub
    Private Sub mapa44(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label44.MouseEnter
        Label43.Hide()
    End Sub
    Private Sub mapa45(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label45.MouseEnter
        Label44.Hide()
    End Sub
    Private Sub mapa46(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label46.MouseEnter
        Label45.Hide()
    End Sub
    Private Sub mapa47(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label47.MouseEnter
        Label46.Hide()
    End Sub
    Private Sub mapa48(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label48.MouseEnter
        Label47.Hide()
    End Sub
    Private Sub mapa49(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label49.MouseEnter
        Label48.Hide()
    End Sub
    Private Sub mapa50(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label50.MouseEnter
        Label49.Hide()
    End Sub
    Private Sub mapa51(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label51.MouseEnter
        Label50.Hide()
    End Sub
    Private Sub mapa52(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label52.MouseEnter
        Label51.Hide()
    End Sub
    Private Sub mapa53(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Label53.MouseEnter
        Label52.Hide()
    End Sub
    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        sTime = sTime.AddSeconds(1)
        Label54.Text = Format(sTime, "mm:ss")
    End Sub
    Private Sub JakHrátToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles JakHrátToolStripMenuItem.Click
        MessageBox.Show("Jdi za zelenou dráhou.")

    End Sub
    Private Sub AutorToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles AutorToolStripMenuItem.Click
        MessageBox.Show("(c) Yana Zabrodskaya")
    End Sub
    Private Sub CheatToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles CheatToolStripMenuItem.Click
        If cheat = False Then
            cheat = True
            Label31.Hide()
            Label9.Hide()
            Label8.Hide()
            Label7.Hide()
            Label6.Hide()
            Label5.Hide()
            Label4.Hide()
            Label34.Hide()
            Label33.Hide()
            Label32.Hide()
            Label30.Hide()
            Label3.Hide()
            Label29.Hide()
            Label28.Hide()
            Label27.Hide()
            Label26.Hide()
            Label25.Hide()
            Label24.Hide()
            Label23.Hide()
            Label22.Hide()
            Label21.Hide()
            Label20.Hide()
            Label2.Hide()
            Label19.Hide()
            Label18.Hide()
            Label17.Hide()
            Label16.Hide()
            Label15.Hide()
            Label14.Hide()
            Label13.Hide()
            Label12.Hide()
            Label11.Hide()
            Label10.Hide()
            Label1.Hide()
        Else
            cheat = False
            Label31.Show()
            Label9.Show()
            Label8.Show()
            Label7.Show()
            Label6.Show()
            Label5.Show()
            Label4.Show()
            Label34.Show()
            Label33.Show()
            Label32.Show()
            Label30.Show()
            Label3.Show()
            Label29.Show()
            Label28.Show()
            Label27.Show()
            Label26.Show()
            Label25.Show()
            Label24.Show()
            Label23.Show()
            Label22.Show()
            Label21.Show()
            Label20.Show()
            Label2.Show()
            Label19.Show()
            Label18.Show()
            Label17.Show()
            Label16.Show()
            Label15.Show()
            Label14.Show()
            Label13.Show()
            Label12.Show()
            Label11.Show()
            Label10.Show()
            Label1.Show()
        End If
    End Sub
    Private Sub AnoToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles AnoToolStripMenuItem.Click
        Close()
    End Sub
    Private Sub RestartToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RestartToolStripMenuItem.Click
        zacatek()
        sTime = "00:00:00"
        Timer1.Start()
    End Sub
End Class
