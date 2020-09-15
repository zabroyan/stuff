Public Class Form1

    'smazat
    Private Sub Button13_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button13.Click
        TextBox1.Text = ""
        TextBox2.Text = ""
        TextBox3.Text = ""
        TextBox4.Text = ""
        TextBox5.Text = ""
        TextBox6.Text = ""
        TextBox7.Text = ""
        TextBox8.Text = ""
        TextBox9.Text = ""
        TextBox10.Text = ""
        TextBox11.Text = ""
        TextBox13.Text = ""
        TextBox12.Text = ""
        TextBox14.Text = ""
        TextBox15.Text = ""
        TextBox16.Text = ""
        TextBox17.Text = ""
        TextBox18.Text = ""
        TextBox19.Text = ""
        TextBox20.Text = ""
        TextBox21.Text = ""
        TextBox22.Text = ""
        TextBox23.Text = ""
        TextBox24.Text = ""
        TextBox25.Text = ""
        TextBox26.Text = ""
        TextBox27.Text = ""
        TextBox28.Text = ""
        TextBox29.Text = ""
        TextBox30.Text = ""
        TextBox31.Text = ""
        TextBox32.Text = ""


        Label1.Text = ""
        Label3.Text = ""
        Label7.Text = ""
        Label12.Text = ""
        Label13.Text = ""
        Label14.Text = ""
        Label15.Text = ""
        Label18.Text = ""
        Label19.Text = ""
        Label34.Text = ""
        Label35.Text = ""
        Label36.Text = ""
        Label37.Text = ""
        Label41.Text = ""
        Label40.Text = ""
        Label39.Text = ""
        Label38.Text = ""
        Label46.Text = ""
        Label45.Text = ""
        Label44.Text = ""
        Label43.Text = ""
        Label42.Text = ""
        Label47.Text = ""
        Label49.Text = ""
        Label52.Text = ""
        Label53.Text = ""
        Label78.Text = ""
        Label77.Text = ""
        Label76.Text = ""
        Label75.Text = ""
        Label74.Text = ""
        Label73.Text = ""
        Label72.Text = ""
        Label71.Text = ""
        Label70.Text = ""
        Label69.Text = ""
        Label68.Text = ""
        Label67.Text = ""


        PictureBox1.Visible = True
        PictureBox2.Visible = True
        PictureBox3.Visible = True
        PictureBox4.Visible = True
        PictureBox5.Visible = True
        PictureBox6.Visible = True
        PictureBox7.Visible = True
        PictureBox8.Visible = True
        PictureBox9.Visible = True
        PictureBox10.Visible = True
        PictureBox11.Visible = True
        PictureBox12.Visible = True

        PictureBox23.Visible = True
        PictureBox20.Visible = True
        PictureBox13.Visible = True
        PictureBox14.Visible = True
        PictureBox15.Visible = True
        PictureBox16.Visible = True
        PictureBox17.Visible = True
        PictureBox18.Visible = True
        PictureBox19.Visible = True
        PictureBox24.Visible = True
        PictureBox21.Visible = True
        PictureBox22.Visible = True

        Chart1.Visible = False
        Button16.Visible = False
        Me.Chart1.Series("Platidla").Points.Clear()
        Chart2.Visible = False
        Button32.Visible = False
        Me.Chart2.Series("vycetka").Points.Clear()
    End Sub

    '<=>
    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click
        TextBox1.Text = Label1.Text
        Label1.Text = ""
    End Sub

    'bin to dec
    Function binToDec(ByVal bin) As Long

        Dim x As Long
        binToDec = 0
        For x = 1 To Len(bin)
            binToDec = binToDec + Val(Mid(bin, x, 1)) * 2 ^ (Len(bin) - x)
        Next

    End Function
    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click
        If IsNumeric(TextBox1.Text) And (TextBox1.Text.Contains(0) = True Or TextBox1.Text.Contains(1) = True) And TextBox1.Text.Contains(2) = False And TextBox1.Text.Contains(3) = False And TextBox1.Text.Contains(4) = False And TextBox1.Text.Contains(5) = False And TextBox1.Text.Contains(6) = False And TextBox1.Text.Contains(7) = False And TextBox1.Text.Contains(8) = False And TextBox1.Text.Contains(9) = False Then
            Label1.Text = binToDec(TextBox1.Text)
        Else
            MsgBox("only 1 and 0", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If

    End Sub

    'dec to bin
    Function decToBin(ByVal dec) As Long
        Dim num_s
        Dim result
        decToBin = 0
        While dec <> 0
            num_s = dec Mod 2
            result = Mid(Str(num_s), 2, 1) + result
            dec = dec \ 2
        End While
        Return result
    End Function
    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click
        If IsNumeric(TextBox1.Text) And TextBox1.Text.Contains(",") = False And TextBox1.Text.Contains(".") = False Then
            Dim result
            Label1.Text = decToBin(TextBox1.Text)
            result = ""
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If


    End Sub

    'hex to dec
    Function hexToDec(ByVal heximal) As Long
        Dim simvol As String
        Dim decCislo As Long
        Dim x As Long
        hexToDec = 0
        For x = 1 To Len(heximal)
            simvol = Mid(heximal, x, 1)
            If UCase(simvol) = "A" Then
                decCislo = 10
            ElseIf UCase(simvol) = "B" Then
                decCislo = 11
            ElseIf UCase(simvol) = "C" Then
                decCislo = 12
            ElseIf UCase(simvol) = "D" Then
                decCislo = 13
            ElseIf UCase(simvol) = "E" Then
                decCislo = 14
            ElseIf UCase(simvol) = "F" Then
                decCislo = 15
            Else
                decCislo = Val(simvol)
            End If
            hexToDec = hexToDec + decCislo * 16 ^ (Len(heximal) - x)
        Next

    End Function
    Private Sub Button4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button4.Click
        If IsNumeric(TextBox1.Text) And TextBox1.Text.Contains(",") = False And TextBox1.Text.Contains(".") = False Or TextBox1.Text.Contains("A") = True Or TextBox1.Text.Contains("B") = True Or TextBox1.Text.Contains("C") = True Or TextBox1.Text.Contains("D") = True Or TextBox1.Text.Contains("E") = True Or TextBox1.Text.Contains("F") = True Then
            Label1.Text = hexToDec(TextBox1.Text)
        Else
            MsgBox("only numbers and A,B,C,D,E,F", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If

    End Sub

    'dec to hex
    Private Sub Button5_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button5.Click
        If IsNumeric(TextBox1.Text) And TextBox1.Text.Contains(",") = False And TextBox1.Text.Contains(".") = False Then
            Dim myhex = Hex(TextBox1.Text)
            Label1.Text = myhex
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If

    End Sub

    'bin to hex
    Private Sub Button7_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button7.Click
        If IsNumeric(TextBox1.Text) And (TextBox1.Text.Contains(0) = True Or TextBox1.Text.Contains(1) = True) And TextBox1.Text.Contains(2) = False And TextBox1.Text.Contains(3) = False And TextBox1.Text.Contains(4) = False And TextBox1.Text.Contains(5) = False And TextBox1.Text.Contains(6) = False And TextBox1.Text.Contains(7) = False And TextBox1.Text.Contains(8) = False And TextBox1.Text.Contains(9) = False Then
            Dim mydec = binToDec(TextBox1.Text)
            Dim myBinToHex = Hex(mydec)
            Label1.Text = myBinToHex
        Else
            MsgBox("only 1 and 0", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If

    End Sub

    'hex to bin
    Private Sub Button8_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button8.Click
        If IsNumeric(TextBox1.Text) And TextBox1.Text.Contains(",") = False And TextBox1.Text.Contains(".") = False Or TextBox1.Text.Contains("A") = True Or TextBox1.Text.Contains("B") = True Or TextBox1.Text.Contains("C") = True Or TextBox1.Text.Contains("D") = True Or TextBox1.Text.Contains("E") = True Or TextBox1.Text.Contains("F") = True Then
            Dim mydec = hexToDec(TextBox1.Text)
            Dim myHexToBin = decToBin(mydec)
            Label1.Text = myHexToBin
        Else
            MsgBox("only numbers and A,B,C,D,E,F", vbExclamation, "try again")
            TextBox1.Text = ""
            Label1.Text = ""
        End If

    End Sub

    'faktorial
    Private Sub Button6_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button6.Click
        Dim faktorial As Double = 1
        If IsNumeric(TextBox2.Text) And TextBox2.Text.Contains(",") = False And TextBox2.Text.Contains(".") = False Then
            For i = 1 To Val(TextBox2.Text)
                faktorial = faktorial * i
            Next i

            Label3.Text = faktorial
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox2.Text = ""
            Label3.Text = ""
        End If

    End Sub

    'kvard rovnice
    Private Sub Button9_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button9.Click

        If IsNumeric(TextBox3.Text) And TextBox3.Text.Contains(",") = False And TextBox3.Text.Contains(".") = False Then
            If IsNumeric(TextBox4.Text) And TextBox4.Text.Contains(",") = False And TextBox4.Text.Contains(".") = False Then
                If IsNumeric(TextBox5.Text) And TextBox5.Text.Contains(",") = False And TextBox5.Text.Contains(".") = False Then
                    Dim a As Double = TextBox3.Text
                    Dim b As Double = TextBox4.Text
                    Dim c As Double = TextBox5.Text
                    Dim D As Double
                    Dim x1 As Double
                    Dim x2 As Double
                    If a = 0 Then
                        x1 = Math.Round(-c / b, 2)
                        Label7.Text = "x1 = " & x1
                    End If
                    If b = 0 Then
                        If -c / a > 0 Then
                            x1 = Math.Round(Math.Sqrt(-c / a), 2)
                            x2 = Math.Round(-Math.Sqrt(-c / a), 2)
                            Label7.Text = "x1 = " & x1 & ";" & vbCrLf & "x2 = " & x2
                        Else
                            MsgBox("nema reseni")
                            TextBox3.Text = ""
                            TextBox4.Text = ""
                            TextBox5.Text = ""
                        End If
                    End If
                    If a <> 0 And b <> 0 Then
                        D = b ^ 2 - 4 * a * c
                        x1 = Math.Round((-b + Math.Sqrt(D)) / (2 * a), 2)
                        x2 = Math.Round((-b - Math.Sqrt(D)) / (2 * a), 2)
                        If D = 0 Then
                            Label7.Text = "x = " & x1
                        ElseIf D > 0 Then
                            Label7.Text = "x1 = " & x1 & ";" & vbCrLf & "x2 = " & x2
                        Else
                            Label7.Text = "nejsou koreni"
                        End If
                    End If

                Else
                    MsgBox("only numbers", vbExclamation, "try again")
                    TextBox3.Text = ""
                    TextBox4.Text = ""
                    TextBox5.Text = ""
                    Label7.Text = ""
                End If
            Else
                MsgBox("only numbers", vbExclamation, "try again")
                TextBox3.Text = ""
                TextBox4.Text = ""
                TextBox5.Text = ""
                Label7.Text = ""
            End If
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox3.Text = ""
            TextBox4.Text = ""
            TextBox5.Text = ""
            Label7.Text = ""
        End If


    End Sub

    'lin rovnice
    Private Sub Button10_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button10.Click
        If IsNumeric(TextBox6.Text) And TextBox6.Text.Contains(",") = False And TextBox6.Text.Contains(".") = False Then
            If IsNumeric(TextBox7.Text) And TextBox7.Text.Contains(",") = False And TextBox7.Text.Contains(".") = False Then
                If IsNumeric(TextBox8.Text) And TextBox8.Text.Contains(",") = False And TextBox8.Text.Contains(".") = False Then
                    If IsNumeric(TextBox9.Text) And TextBox9.Text.Contains(",") = False And TextBox9.Text.Contains(".") = False Then
                        If IsNumeric(TextBox10.Text) And TextBox10.Text.Contains(",") = False And TextBox10.Text.Contains(".") = False Then
                            If IsNumeric(TextBox11.Text) And TextBox11.Text.Contains(",") = False And TextBox11.Text.Contains(".") = False Then
                                Dim a As Double = TextBox6.Text
                                Dim b As Double = TextBox7.Text
                                Dim c As Double = TextBox8.Text
                                Dim d As Double = TextBox9.Text
                                Dim g As Double = TextBox10.Text
                                Dim f As Double = TextBox11.Text
                                Dim x As Double
                                Dim y As Double

                                x = Math.Round((f * b - g * c) / (b * d - g * a), 2)
                                y = Math.Round((f * a - d * c) / (a * g - b * d), 2)
                                If (b * d - g * a) = 0 Then
                                    Label12.Text = "nema reseni"
                                    TextBox6.Text = ""
                                    TextBox7.Text = ""
                                    TextBox8.Text = ""
                                    TextBox9.Text = ""
                                    TextBox10.Text = ""
                                    TextBox11.Text = ""
                                Else
                                    Label12.Text = "x = " & x & ";" & vbCrLf & "y = " & y
                                End If

                            Else
                                MsgBox("only numbers", vbExclamation, "try again")
                                TextBox6.Text = ""
                                TextBox7.Text = ""
                                TextBox8.Text = ""
                                TextBox9.Text = ""
                                TextBox10.Text = ""
                                TextBox11.Text = ""
                                Label12.Text = ""
                            End If
                        Else
                            MsgBox("only numbers", vbExclamation, "try again")
                            TextBox6.Text = ""
                            TextBox7.Text = ""
                            TextBox8.Text = ""
                            TextBox9.Text = ""
                            TextBox10.Text = ""
                            TextBox11.Text = ""
                            Label12.Text = ""
                        End If
                    Else
                        MsgBox("only numbers", vbExclamation, "try again")
                        TextBox6.Text = ""
                        TextBox7.Text = ""
                        TextBox8.Text = ""
                        TextBox9.Text = ""
                        TextBox10.Text = ""
                        TextBox11.Text = ""
                        Label12.Text = ""
                    End If
                Else
                    MsgBox("only numbers", vbExclamation, "try again")
                    TextBox6.Text = ""
                    TextBox7.Text = ""
                    TextBox8.Text = ""
                    TextBox9.Text = ""
                    TextBox10.Text = ""
                    TextBox11.Text = ""
                    Label12.Text = ""
                End If
            Else
                MsgBox("only numbers", vbExclamation, "try again")
                TextBox6.Text = ""
                TextBox7.Text = ""
                TextBox8.Text = ""
                TextBox9.Text = ""
                TextBox10.Text = ""
                TextBox11.Text = ""
                Label12.Text = ""
            End If
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox6.Text = ""
            TextBox7.Text = ""
            TextBox8.Text = ""
            TextBox9.Text = ""
            TextBox10.Text = ""
            TextBox11.Text = ""
            Label12.Text = ""
        End If
    End Sub

    'dec to zlomek
    Private Sub Button11_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button11.Click
        If (IsNumeric(TextBox12.Text) And TextBox12.Text.Contains(",") = False And TextBox12.Text.Contains(".") = False) Or Len(TextBox12.Text) = 0 Then
            If (IsNumeric(TextBox13.Text) And TextBox13.Text.Contains(",") = False And TextBox13.Text.Contains(".") = False) Or Len(TextBox13.Text) = 0 Then
                Dim zlomek As Double = 0
                zlomek = Len(TextBox13.Text)
                Dim citatel As Integer
                Dim jmenovatel As Integer

                If Len(TextBox12.Text) = 0 Then
                    TextBox12.Text = 0
                End If
                If Len(TextBox13.Text) = 0 Then
                    TextBox13.Text = 0
                End If

                citatel = TextBox12.Text * 10 ^ zlomek + TextBox13.Text
                jmenovatel = 10 ^ zlomek

                For i = citatel To 1 Step -1
                    If citatel Mod i = 0 And jmenovatel Mod i = 0 Then
                        citatel = citatel / i
                        jmenovatel = jmenovatel / i

                    End If
                    Label13.Text = citatel
                    Label14.Text = jmenovatel
                    Label15.Text = "------"
                Next i

                If jmenovatel = 1 Then
                    Label13.Text = TextBox12.Text
                    Label14.Text = ""
                    Label15.Text = ""
                End If

            Else
                MsgBox("only numbers", vbExclamation, "try again")
                TextBox12.Text = ""
                TextBox13.Text = ""
                Label13.Text = ""
                Label14.Text = ""
                Label15.Text = ""
            End If
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox12.Text = ""
            TextBox13.Text = ""
            Label13.Text = ""
            Label14.Text = ""
            Label15.Text = ""
        End If
    End Sub

    'prvocisla
    Private Sub Button12_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button12.Click
        If IsNumeric(TextBox14.Text) And TextBox14.Text.Contains(",") = False And TextBox14.Text.Contains(".") = False Then
            Dim number As Integer = TextBox14.Text
            Dim prvocisla As String = ""
            Dim ifPrvocislo As Integer = 0

            If number < 0 Then
                number = -number
            End If

            For i = 2 To number - 1
                If number Mod i = 0 Then
                    prvocisla = prvocisla & " x " & i
                    ifPrvocislo = ifPrvocislo + i
                    number = number / i
                    Label19.Text = TextBox14.Text & " ="
                    i -= 1
                End If
            Next i
            If ifPrvocislo = 0 And (TextBox14.Text > 1 Or TextBox14.Text < 1) And TextBox14.Text <> -1 Then
                prvocisla = "to je prvocislo"
                Label19.Text = ""
            End If
            Label18.Text = prvocisla
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox14.Text = ""
            Label19.Text = ""
        End If
    End Sub

    'platidla
    Private Sub Button14_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button14.Click
        Me.Chart1.Series("Platidla").Points.Clear()
        If TextBox15.Text = "" Or Val(TextBox15.Text) = 0 Then
            TextBox15.Text = 0
            Label34.Text = 0
        ElseIf IsNumeric(TextBox15.Text) Then
            Label34.Text = TextBox15.Text * 5000
            Me.Chart1.Series("Platidla").Points.AddXY("5000", Label34.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox15.Text = ""
        End If
        If TextBox16.Text = "" Or Val(TextBox16.Text) = 0 Then
            TextBox16.Text = 0
            Label35.Text = 0
        ElseIf IsNumeric(TextBox16.Text) Then
            Label35.Text = TextBox16.Text * 2000
            Me.Chart1.Series("Platidla").Points.AddXY("2000", Label35.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox16.Text = ""
        End If
        If TextBox17.Text = "" Or Val(TextBox17.Text) = 0 Then
            TextBox17.Text = 0
            Label36.Text = 0
        ElseIf IsNumeric(TextBox17.Text) Then
            Label36.Text = TextBox17.Text * 1000
            Me.Chart1.Series("Platidla").Points.AddXY("1000", Label36.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox17.Text = ""
        End If
        If TextBox20.Text = "" Or Val(TextBox20.Text) = 0 Then
            TextBox20.Text = 0
            Label37.Text = 0
        ElseIf IsNumeric(TextBox20.Text) Then
            Label37.Text = TextBox20.Text * 500
            Me.Chart1.Series("Platidla").Points.AddXY("500", Label37.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox20.Text = ""
        End If
        If TextBox19.Text = "" Or Val(TextBox19.Text) = 0 Then
            TextBox19.Text = 0
            Label41.Text = 0
        ElseIf IsNumeric(TextBox19.Text) Then
            Label41.Text = TextBox19.Text * 200
            Me.Chart1.Series("Platidla").Points.AddXY("200", Label41.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox19.Text = ""
        End If
        If TextBox18.Text = "" Or Val(TextBox18.Text) = 0 Then
            TextBox18.Text = 0
            Label40.Text = 0
        ElseIf IsNumeric(TextBox18.Text) Then
            Label40.Text = TextBox18.Text * 100
            Me.Chart1.Series("Platidla").Points.AddXY("100", Label40.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox18.Text = ""
        End If
        If TextBox26.Text = "" Or Val(TextBox26.Text) = 0 Then
            TextBox26.Text = 0
            Label39.Text = 0
        ElseIf IsNumeric(TextBox26.Text) Then
            Label39.Text = TextBox26.Text * 50
            Me.Chart1.Series("Platidla").Points.AddXY("50", Label39.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox26.Text = ""
        End If
        If TextBox25.Text = "" Or Val(TextBox25.Text) = 0 Then
            TextBox25.Text = 0
            Label38.Text = 0
        ElseIf IsNumeric(TextBox25.Text) Then
            Label38.Text = TextBox25.Text * 20
            Me.Chart1.Series("Platidla").Points.AddXY("20", Label38.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox25.Text = ""
        End If
        If TextBox24.Text = "" Or Val(TextBox24.Text) = 0 Then
            TextBox24.Text = 0
            Label46.Text = 0
        ElseIf IsNumeric(TextBox24.Text) Then
            Label46.Text = TextBox24.Text * 10
            Me.Chart1.Series("Platidla").Points.AddXY("10", Label46.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox24.Text = ""
        End If
        If TextBox23.Text = "" Or Val(TextBox23.Text) = 0 Then
            TextBox23.Text = 0
            Label45.Text = 0
        ElseIf IsNumeric(TextBox23.Text) Then
            Label45.Text = TextBox23.Text * 5
            Me.Chart1.Series("Platidla").Points.AddXY("5", Label45.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox23.Text = ""
        End If
        If TextBox22.Text = "" Or Val(TextBox22.Text) = 0 Then
            TextBox22.Text = 0
            Label44.Text = 0
        ElseIf IsNumeric(TextBox22.Text) Then
            Label44.Text = TextBox22.Text * 2
            Me.Chart1.Series("Platidla").Points.AddXY("2", Label44.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox22.Text = ""
        End If
        If TextBox21.Text = "" Or Val(TextBox21.Text) = 0 Then
            TextBox21.Text = 0
            Label43.Text = 0
        ElseIf IsNumeric(TextBox21.Text) Then
            Label43.Text = TextBox21.Text * 1
            Me.Chart1.Series("Platidla").Points.AddXY("1", Label43.Text)
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox21.Text = ""
        End If
        If (IsNumeric(TextBox15.Text) Or TextBox15.Text.Contains("")) And (IsNumeric(TextBox16.Text) Or TextBox16.Text.Contains("")) And (IsNumeric(TextBox17.Text) Or TextBox17.Text.Contains("")) And (IsNumeric(TextBox18.Text) Or TextBox18.Text.Contains("")) And (IsNumeric(TextBox19.Text) Or TextBox19.Text.Contains("")) And (IsNumeric(TextBox20.Text) Or TextBox20.Text.Contains("")) And (IsNumeric(TextBox21.Text) Or TextBox21.Text.Contains("")) And (IsNumeric(TextBox22.Text) Or TextBox22.Text.Contains("")) And (IsNumeric(TextBox23.Text) Or TextBox23.Text.Contains("")) And (IsNumeric(TextBox24.Text) Or TextBox24.Text.Contains("")) And (IsNumeric(TextBox25.Text) Or TextBox25.Text.Contains("")) And (IsNumeric(TextBox26.Text) Or TextBox26.Text.Contains("")) Then
            ' Label42.Text = TextBox15.Text * 5000 + TextBox16.Text * 2000 + TextBox17.Text * 1000 + TextBox20.Text * 500 + TextBox19.Text * 200 + TextBox18.Text * 100 + TextBox26.Text * 50 + TextBox25.Text * 20 + TextBox24.Text * 10 + TextBox23.Text * 5 + TextBox22.Text * 2 + TextBox21.Text * 1
            Label42.Text = Val(Label34.Text) + Val(Label35.Text) + Val(Label36.Text) + Val(Label37.Text) + Val(Label38.Text) + Val(Label39.Text) + Val(Label40.Text) + Val(Label41.Text) + Val(Label43.Text) + Val(Label44.Text) + Val(Label45.Text) + Val(Label46.Text)
        End If


    End Sub
    'diagram
    Private Sub Button15_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button15.Click
        Button16.Visible = True

        Chart1.Visible = True
        PictureBox1.Visible = False
        PictureBox2.Visible = False
        PictureBox3.Visible = False
        PictureBox4.Visible = False
        PictureBox5.Visible = False
        PictureBox6.Visible = False
        PictureBox7.Visible = False
        PictureBox8.Visible = False
        PictureBox9.Visible = False
        PictureBox10.Visible = False
        PictureBox11.Visible = False
        PictureBox12.Visible = False
    End Sub
    'zpatky
    Private Sub Button16_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button16.Click
        Chart1.Visible = False
        Button16.Visible = False
        PictureBox1.Visible = True
        PictureBox2.Visible = True
        PictureBox3.Visible = True
        PictureBox4.Visible = True
        PictureBox5.Visible = True
        PictureBox6.Visible = True
        PictureBox7.Visible = True
        PictureBox8.Visible = True
        PictureBox9.Visible = True
        PictureBox10.Visible = True
        PictureBox11.Visible = True
        PictureBox12.Visible = True
    End Sub

    'paskaluv trojuhelnik
    Private Sub Button17_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button17.Click
        Dim n As Integer  'Number of rows
        Dim i, j As Integer 'Counters
        TextBox27.Text = ""
        n = Val(InputBox("pocet rady"))
        If IsNumeric(n) Then
            For i = 0 To n - 1
                TextBox27.Text += (Space(n - i))
                For j = 0 To i
                    TextBox27.Text += Trim(Str(nCr(i, j))) + " "
                Next j
                TextBox27.Text += vbNewLine
            Next i
        Else
            MsgBox("only numbers", vbExclamation, "try again")
        End If

    End Sub
    Private Function nCr(ByVal n As Integer, ByVal r As Integer) As Long
        If (n = r) Then
            nCr = 1
        Else
            nCr = Factorial(n) / (Factorial(n - r) * Factorial(r))
        End If
    End Function
    Private Function Factorial(ByVal n As Integer) As Long
        Dim i As Integer
        Factorial = 1
        If IsNumeric(n) Then
            If n <> 0 Then
                For i = 2 To n
                    Factorial = Factorial * i
                Next i
            End If
        Else
            MsgBox("only numbers", vbExclamation, "try again")
        End If

    End Function

    'pole
    Dim pole As New List(Of Integer)
    Private Sub Button18_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button18.Click
        If IsNumeric(TextBox28.Text) Then
            pole.Add(Val(TextBox28.Text))
            Label47.Text = "ted' v poli jsou " & pole.Count & " cisel."
            TextBox28.Text = ""
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox28.Text = ""
            Label47.Text = ""
        End If

    End Sub
    'max
    Private Sub Button19_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button19.Click
        If pole.Count >= 1 Then
            pole.Sort()
            Dim max As Integer = pole(pole.Count - 1)
            Label47.Text = max
        Else
            MsgBox("list is empty")
        End If

    End Sub
    'min
    Private Sub Button20_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button20.Click
        If pole.Count >= 1 Then
            pole.Sort()
            Dim min As Integer = pole(0)
            Label47.Text = min
        Else
            MsgBox("list is empty")
        End If

    End Sub
    Private Sub Button24_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button24.Click
        pole.Clear()
        Label47.Text = ""
    End Sub

    'razeni v poli

    'dodat
    Private Sub Button23_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button23.Click
        If IsNumeric(TextBox29.Text) Then
            pole.Add(TextBox29.Text)
            Label49.Text = "ted' v poli jsou " & pole.Count & " cisel."
            TextBox29.Text = ""
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox28.Text = ""
            Label47.Text = ""
        End If


    End Sub
    'razeni
    Private Sub Button21_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button21.Click
        Label49.Text = ""
        If pole.Count >= 1 Then
            pole.Sort()
            For i = 0 To pole.Count - 1
                Dim razeni = pole(i)
                Label49.Text = Label49.Text & " " & razeni
            Next
        Else
            MsgBox("list is empty")
        End If
    End Sub
    Private Sub Button22_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button22.Click
        pole.Clear()
        Label49.Text = ""
    End Sub

    'prunik a sjednoceni
    Dim pole1 As New List(Of Integer)
    Dim pole2 As New List(Of Integer)
    'dodat
    Private Sub Button29_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button29.Click

        If IsNumeric(TextBox31.Text) And IsNumeric(TextBox30.Text) Then
            pole1.Add(TextBox30.Text)
            Label52.Text = "ted' v 1. poli jsou " & pole1.Count & " cisel."
            pole2.Add(TextBox31.Text)
            Label53.Text = "ted' v 2. poli jsou " & pole2.Count & " cisel."
            TextBox31.Text = ""
            TextBox30.Text = ""
        ElseIf IsNumeric(TextBox31.Text) Then
            pole2.Add(TextBox31.Text)
            Label53.Text = "ted' v 2. poli jsou " & pole2.Count & " cisel."
            TextBox31.Text = ""
        ElseIf IsNumeric(TextBox30.Text) Then
            pole1.Add(TextBox30.Text)
            Label52.Text = "ted' v 1. poli jsou " & pole1.Count & " cisel."
            TextBox30.Text = ""
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox30.Text = ""
            TextBox31.Text = ""
        End If

    End Sub

    Private Sub Button27_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button27.Click
        pole1.Clear()
        Label52.Text = ""
    End Sub
    Private Sub Button28_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button28.Click
        pole2.Clear()
        Label53.Text = ""
    End Sub
    'prunik
    Private Sub Button25_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button25.Click
        Label52.Text = ""
        Label53.Text = ""
        If pole1.Count >= 1 And pole2.Count >= 1 Then
            Dim polePrunik As New List(Of Integer)
            For i = 0 To pole1.Count - 1
                For j = 0 To pole2.Count - 1
                    If pole1(i) = pole2(j) Then
                        polePrunik.Add(pole1(i))
                    End If
                Next
            Next
            If polePrunik.Count >= 1 Then
                polePrunik.Sort()
                For n = 0 To polePrunik.Count - 1
                    Label52.Text = Label52.Text & " " & polePrunik(n)
                Next
            Else
                Label52.Text = "neni prunik"
            End If

        Else
            MsgBox("list(s) is empty")
        End If


    End Sub
    'sjednoceni
    Private Sub Button26_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button26.Click
        Label52.Text = ""
        Label53.Text = ""
        If pole1.Count >= 1 Or pole2.Count >= 1 Then
            Dim poleSjednoceni As New List(Of Integer)
            For i = 0 To pole2.Count - 1
                poleSjednoceni.Add(pole2(i))
            Next
            For i = 0 To pole1.Count - 1
                poleSjednoceni.Add(pole1(i))
            Next
            poleSjednoceni.Sort()
            For i = 0 To poleSjednoceni.Count - 1
                Label52.Text = Label52.Text & " " & poleSjednoceni(i)
            Next
        Else
            MsgBox("lists are empty")
        End If

    End Sub

    'vycetka(2)
    Private Sub Button30_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button30.Click
        Me.Chart2.Series("vycetka").Points.Clear()
        If IsNumeric(TextBox32.Text) Then
            Dim celkem As Integer = TextBox32.Text
            If celkem >= 5000 Then
                Label78.Text = celkem \ 5000
                celkem = celkem Mod 5000
                Me.Chart2.Series("vycetka").Points.AddXY("5000", Label78.Text * 5000)
            End If
            If celkem >= 2000 Then
                Label77.Text = celkem \ 2000
                celkem = celkem Mod 2000
                Me.Chart2.Series("vycetka").Points.AddXY("2000", Label77.Text * 2000)
            End If
            If celkem >= 1000 Then
                Label76.Text = celkem \ 1000
                celkem = celkem Mod 1000
                Me.Chart2.Series("vycetka").Points.AddXY("1000", Label76.Text * 1000)
            End If
            If celkem >= 500 Then
                Label75.Text = celkem \ 500
                celkem = celkem Mod 500
                Me.Chart2.Series("vycetka").Points.AddXY("500", Label75.Text * 500)
            End If
            If celkem >= 200 Then
                Label74.Text = celkem \ 200
                celkem = celkem Mod 200
                Me.Chart2.Series("vycetka").Points.AddXY("200", Label74.Text * 200)
            End If
            If celkem >= 100 Then
                Label73.Text = celkem \ 100
                celkem = celkem Mod 100
                Me.Chart2.Series("vycetka").Points.AddXY("100", Label73.Text * 100)
            End If
            If celkem >= 50 Then
                Label72.Text = celkem \ 50
                celkem = celkem Mod 50
                Me.Chart2.Series("vycetka").Points.AddXY("50", Label72.Text * 50)
            End If
            If celkem >= 20 Then
                Label71.Text = celkem \ 20
                celkem = celkem Mod 20
                Me.Chart2.Series("vycetka").Points.AddXY("20", Label71.Text * 20)
            End If
            If celkem >= 10 Then
                Label70.Text = celkem \ 10
                celkem = celkem Mod 10
                Me.Chart2.Series("vycetka").Points.AddXY("10", Label70.Text * 10)
            End If
            If celkem >= 5 Then
                Label69.Text = celkem \ 5
                celkem = celkem Mod 5
                Me.Chart2.Series("vycetka").Points.AddXY("5", Label69.Text * 5)
            End If
            If celkem >= 2 Then
                Label68.Text = celkem \ 2
                celkem = celkem Mod 2
                Me.Chart2.Series("vycetka").Points.AddXY("2", Label68.Text * 2)
            End If
            If celkem >= 1 Then
                Label67.Text = celkem \ 1
                celkem = celkem Mod 1
                Me.Chart2.Series("vycetka").Points.AddXY("1", Label67.Text * 1)
            End If
        Else
            MsgBox("only numbers", vbExclamation, "try again")
            TextBox32.Text = ""
        End If
    End Sub

    Private Sub Button31_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button31.Click
        Chart2.Visible = True
        Button32.Visible = True
        PictureBox23.Visible = False
        PictureBox20.Visible = False
        PictureBox13.Visible = False
        PictureBox14.Visible = False
        PictureBox15.Visible = False
        PictureBox16.Visible = False
        PictureBox17.Visible = False
        PictureBox18.Visible = False
        PictureBox19.Visible = False
        PictureBox24.Visible = False
        PictureBox21.Visible = False
        PictureBox22.Visible = False

    End Sub

    Private Sub Button32_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button32.Click
        Chart2.Visible = False
        Button32.Visible = False
        PictureBox23.Visible = True
        PictureBox20.Visible = True
        PictureBox13.Visible = True
        PictureBox14.Visible = True
        PictureBox15.Visible = True
        PictureBox16.Visible = True
        PictureBox17.Visible = True
        PictureBox18.Visible = True
        PictureBox19.Visible = True
        PictureBox24.Visible = True
        PictureBox21.Visible = True
        PictureBox22.Visible = True
    End Sub

 
    Private Sub TextBox14_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox14.TextChanged
        AcceptButton = Button12
    End Sub

    Private Sub TextBox29_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox29.TextChanged
        AcceptButton = Button23
    End Sub

    Private Sub TextBox28_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox28.TextChanged
        AcceptButton = Button18
    End Sub

    Private Sub TextBox30_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox30.TextChanged
        AcceptButton = Button29
    End Sub

    Private Sub TextBox31_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox31.TextChanged
        AcceptButton = Button29
    End Sub

    Private Sub TextBox2_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox2.TextChanged
        AcceptButton = Button6
    End Sub

    Private Sub TextBox3_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox3.TextChanged
        AcceptButton = Button9
    End Sub

    Private Sub TextBox4_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox4.TextChanged
        AcceptButton = Button9
    End Sub

    Private Sub TextBox5_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox5.TextChanged
        AcceptButton = Button9
    End Sub

    Private Sub TextBox12_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox12.TextChanged
        AcceptButton = Button11
    End Sub

    Private Sub TextBox13_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox13.TextChanged
        AcceptButton = Button11
    End Sub

    Private Sub TextBox6_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox6.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox7_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox7.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox8_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox8.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox9_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox9.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox10_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox10.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox11_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox11.TextChanged
        AcceptButton = Button10
    End Sub

    Private Sub TextBox32_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox32.TextChanged
        AcceptButton = Button30
        Label78.Text = ""
        Label77.Text = ""
        Label76.Text = ""
        Label75.Text = ""
        Label74.Text = ""
        Label73.Text = ""
        Label72.Text = ""
        Label71.Text = ""
        Label70.Text = ""
        Label69.Text = ""
        Label68.Text = ""
        Label67.Text = ""
        Me.Chart2.Series("vycetka").Points.Clear()
    End Sub

    Private Sub TextBox15_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox15.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox16_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox16.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox17_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox17.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox18_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox18.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox19_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox19.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox20_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox20.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox21_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox21.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox22_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox22.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox23_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox23.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox24_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox24.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox25_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox25.TextChanged
        AcceptButton = Button14
    End Sub
    Private Sub TextBox26_TextChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TextBox26.TextChanged
        AcceptButton = Button14
    End Sub


End Class
